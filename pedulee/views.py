import datetime
from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ClothForm, ExtendedUserCreationForm
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
from .models import Cloth

# Create your views here.
@login_required(login_url="/sign-in")
def show_home(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "home.html", context)

@login_required(login_url="/sign-in")
def show_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "history.html", context)

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

    context = {'form' : form, 'profile_form' : profile_form}
    return render(request, 'signup.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("pedulee:home"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Username or Password is wrong!')
    context = {}
    return render(request, 'signin.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('pedulee:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/sign-in")
def show_clothes_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "clothes-history.html", context)

@login_required(login_url="/sign-in")
def show_money_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "money-history.html", context)

@login_required(login_url="/sign-in")
def show_groceries_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "groceries-history.html", context)

@login_required(login_url="/sign-in")
def show_blood_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "blood-history.html", context)

@login_required(login_url="/sign-in")
def show_volunteer_history(request):
    username = request.user
    context = {
        'username': username,
    }
    return render(request, "volunteer-history.html", context)

def show_json_cloth(request):
    data = Cloth.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url="/sign-in")
def create_cloth(request):
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
            cloth.save()
            return render(request, 'donasi-pakaian.html', context)

    return render(request, 'donasi-pakaian.html', context)

@csrf_exempt
def delete_cloth(request, i):
    if request.method == "DELETE":
        cloth = Cloth.objects.get(id=i)
        cloth.delete()
    return HttpResponse(b"DELETE")

def show_projects(request):
    context = {}
    return render(request, 'projects.html', context)

