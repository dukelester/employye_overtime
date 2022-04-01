# Generated by Django 4.0.3 on 2022-04-01 11:12

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=65, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=40, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_hr', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('user_type', models.CharField(choices=[('Hr', 'Hr'), ('Employee', 'Employee')], max_length=34)),
                ('profile_image', models.ImageField(blank=True, default=authentication.models.get_default_profile_image, max_length=255, null=True, upload_to=authentication.models.profile_image_filepath)),
                ('hide_email', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
    ]
