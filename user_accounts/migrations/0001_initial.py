# Generated by Django 5.2 on 2025-04-26 03:22

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import location_field.models.plain
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('company', 'Company'), ('customer', 'Customer'), ('guest', 'Guest')], default='guest', max_length=10, verbose_name='User Type')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='Company Name')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, verbose_name='Location')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('bio', models.TextField(verbose_name='Bio')),
                ('logo', models.ImageField(blank=True, upload_to='company_logos/', verbose_name='Logo')),
                ('website', models.URLField(blank=True, verbose_name='Website')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Company Profile',
                'verbose_name_plural': 'Company Profiles',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100, verbose_name='اسم المتجر')),
                ('phone', models.CharField(max_length=20, verbose_name='رقم الهاتف')),
                ('address', models.TextField(verbose_name='العنوان')),
                ('city', models.CharField(max_length=100, verbose_name='المدينة')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='البلد')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, verbose_name='الموقع')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'عميل',
                'verbose_name_plural': 'العملاء',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100, verbose_name='Store Name')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, verbose_name='Location')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('bio', models.TextField(blank=True, verbose_name='Bio')),
                ('logo', models.ImageField(blank=True, upload_to='store_logos/', verbose_name='Logo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Customer Profile',
                'verbose_name_plural': 'Customer Profiles',
            },
        ),
    ]
