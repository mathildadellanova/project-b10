# Generated by Django 4.1 on 2022-10-29 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedulee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('link', models.CharField(max_length=256)),
                ('amount', models.BigIntegerField()),
                ('akhir_waktu', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cloth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('cloth_model', models.CharField(choices=[('Kemeja', 'Kemeja'), ('Kaos', 'Kaos'), ('Celana', 'Celana'), ('Rok', 'Rok'), ('Sepatu', 'Sepatu'), ('Aksesoris', 'Aksesoris'), ('Lainnya', 'Lainnya')], default='Kemeja', max_length=30)),
                ('material', models.CharField(choices=[('Katun', 'Katun'), ('Linen', 'Linen'), ('Denim', 'Denim'), ('Kulit', 'Kulit'), ('Polyester', 'Polyester'), ('Suede', 'Suede'), ('Sutra', 'Sutra'), ('Velvet', 'Velvet'), ('Rajut', 'Rajut'), ('Rayon', 'Rayon'), ('Jersey', 'Jersey'), ('Twistcone', 'Twistcone'), ('Lainnya', 'Lainnya')], default='Katun', max_length=30)),
                ('type', models.CharField(choices=[('Perempuan', 'Perempuan'), ('Laki-laki', 'Laki-laki'), ('Anak perempuan', 'Anak perempuan'), ('Anak laki-laki', 'Anak laki-laki')], default='Perempuan', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('golongan', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')], max_length=30)),
                ('rhesus', models.CharField(choices=[('+', '+'), ('-', '-')], max_length=30)),
                ('penyakit_bawaan', models.CharField(max_length=30)),
                ('lokasi_donor', models.CharField(choices=[('Jakarta', 'Jakarta'), ('Depok', 'Depok'), ('Bogor', 'Bogor'), ('bandung', 'Bandung')], max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
