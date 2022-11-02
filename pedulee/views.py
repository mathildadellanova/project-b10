import datetime
import json
from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ClothForm, ExtendedUserCreationForm, VolunteerForm, MoneyForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProfileForm
from .models import Cloth, Project, Volunteer, Money

# Create your views here.
def my_render(request, page, context:dict):
    context['username'] = request.user
    return render(request, page, context)


class HomeViews:
    @staticmethod
    def index(request):
        projects = Project.objects.all()
        context = {
            'projects': projects,
        }
        return my_render(request, "home.html", context)

class UserViews:
    @staticmethod
    def register(request):
        if request.method == "POST":
            form = ExtendedUserCreationForm(request.POST)
            profile_form = ProfileForm(request.POST)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                messages.success(request, 'Your account has been successfully created!')
                return redirect('pedulee:login')
        else:
            form = ExtendedUserCreationForm()
            profile_form = ProfileForm()

        context = {'form':form, 'profile_form':profile_form}
        return my_render(request, 'signup.html', context)

    def login(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) # melakukan login terlebih dahulu
                response = HttpResponseRedirect(reverse("pedulee:home")) # membuat response
                response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
                return response
            else:
                messages.info(request, 'Username or Password is wrong!')
        context = {}
        return my_render(request, 'signin.html', context)

    def profile(request):
        # user = User
        context = {}
        return my_render(request, 'profile.html', context)

    def logout(request):
        logout(request)
        response = HttpResponseRedirect(reverse('pedulee:login'))
        response.delete_cookie('last_login')
        return response

class HistoryView:
    @staticmethod
    @login_required(login_url="/sign-in")
    def show_history(request):
        context = {}
        return my_render(request, "history.html", context)


    @staticmethod
    @login_required(login_url="/sign-in")
    def show_clothes(request):
        if request.user.is_staff:
            context = {
                'username' : request.user,
                'status' : 'staff'
            }
        else:
            context = {
                'username': request.user,
                'status' : 'non-staff'
            }
        return my_render(request, "cloth/history.html", context)

    @staticmethod
    @login_required(login_url="/sign-in")
    def show_money(request):
        context = {}
        return my_render(request, "money/history.html", context)

    @staticmethod
    @login_required(login_url="/sign-in")
    def show_groceries(request):
        context = {}
        return my_render(request, "groceries/history.html", context)

    @staticmethod
    @login_required(login_url="/sign-in")
    def show_blood(request):
        context = {}
        return my_render(request, "blood/history.html", context)

    @staticmethod
    @login_required(login_url="/sign-in")
    def show_volunteer(request):
        context = {}
        return my_render(request, "volunteer/history.html", context)

class ProjectView:
    @staticmethod
    def show(request):
        projects = Project.objects.all()
        context = {
            'projects': projects,
        }
        return my_render(request, 'projects/index.html', context)

class ClothesView:
    @staticmethod
    @login_required(login_url="/sign-in")
    def show(request):
        form = ClothForm()
        username = request.user
        visit = None
        request.session.modified = True
        if 'visit_clothes' in request.session:
            times_donate = int(request.session['visit_clothes'])
            times_donate += 1
            request.session['visit_clothes'] = times_donate
            if times_donate < 1:
                visit = 'Welcome'
            else:
                visit = 'Welcome back'
        else:
            request.session['visit_clothes'] = 0
            visit = 'Welcome'
        context = {
            'username': username,
            'form' : form,
            'visit' : visit,
        }
        return render(request, "cloth/form.html", context)

    @staticmethod
    def show_json(request):
        if request.user.is_staff:
            data_user = Cloth.objects.all()
        else:
            data_user = Cloth.objects.filter(user = request.user)
        return HttpResponse(serializers.serialize("json", data_user), content_type="application/json")

    @staticmethod
    @login_required(login_url="/sign-in")
    def create(request):
        form = ClothForm()
        visit = None
        request.session.modified = True

        if 'visit_clothes' in request.session:
            times_donate = int(request.session['visit_clothes'])
            times_donate += 1
            request.session['visit_clothes'] = times_donate
            if times_donate < 1:
                visit = 'Welcome'
            else:
                visit = 'Welcome back'
        else:
            request.session['visit_clothes'] = 0
            visit = 'Welcome'

        context = {'form': form, 'username': request.user, 'visit' : visit, 'name' : request.user.get_full_name()}
        if request.method == 'POST':
            form = ClothForm(request.POST)
            if form.is_valid():
                cloth = form.save(commit=False)
                cloth.user = request.user
                cloth.username = request.user.get_username()
                cloth.save()
                return my_render(request, 'cloth/form.html', context)

        return my_render(request, 'cloth/form.html', context)

    @staticmethod
    @csrf_exempt
    def delete (request, i):
        if request.method == "DELETE":
            cloth = Cloth.objects.get(id=i)
            cloth.delete()
        return HttpResponse(b"DELETE")

class VolunteerView:
    @staticmethod
    @login_required(login_url="/sign-in")
    def create(request):
        form = VolunteerForm()
        if request.method == 'POST':
            form = VolunteerForm(request.POST)
            print(form)
            if form.is_valid():
                print('isvalid')
                volunteer = form.save(commit=False)
                volunteer.user = request.user
                volunteer.save()
                return HttpResponse(b"CREATED", status=201)

        projects = Project.objects.all()
        context = {
            'form': form,
            'projects': serializers.serialize('json', projects)
        }
        return my_render(request, 'volunteer/form.html', context)

    @staticmethod
    def show_json(request):
        data = Volunteer.objects.filter(user = request.user).prefetch_related('project')
        response = []
        for item in data:
            response.append({
                'id': item.pk,
                'title': item.project.title,
                'amount': item.project.amount,
                'divisi': item.divisi
            })
            print(item.project.title, item.project.amount)
        return HttpResponse(json.dumps(response), content_type="application/json")

    @staticmethod
    @csrf_exempt
    def delete (request, i):
        print('deleting ', i)
        if request.method == "DELETE":
            volunteer = Volunteer.objects.get(id=i)
            volunteer.delete()
        return HttpResponse(b"DELETE")

class MoneyView:
    @staticmethod
    @login_required(login_url="/sign-in")
    def create(request):
        form = MoneyForm()
        if request.method == 'POST':
            form = MoneyForm(request.POST)
            print(form)
            if form.is_valid():
                print('isvalid')
                money = form.save(commit=False)
                money.user = request.user
                money.save()
                context = {
                    'form': form
                }
                return render(request, 'money/form.html', context)

        context = {
            'form': form
        }
        return my_render(request, 'money/form.html', context)

    @staticmethod
    def show_json(request):
        if request.user.is_staff:
            data_user = Money.objects.all()
        else:
            data_user = Money.objects.filter(user = request.user)
        return HttpResponse(serializers.serialize("json", data_user), content_type="application/json")

    @staticmethod
    @csrf_exempt
    def delete (request, i):
        if request.method == "DELETE":
            money = Money.objects.get(pk=i)
            money.delete()
        return HttpResponse(b"DELETE")

    