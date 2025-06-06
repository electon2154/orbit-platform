# Generated by Django 5.2 on 2025-04-26 03:22

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الفئة')),
                ('description', models.TextField(blank=True, verbose_name='الوصف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
            ],
            options={
                'verbose_name': 'فئة',
                'verbose_name_plural': 'الفئات',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم المنتج')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='رمز المنتج')),
                ('description', ckeditor.fields.RichTextField(verbose_name='الوصف')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='السعر')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='المخزون')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='الصورة')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_catalog.category', verbose_name='الفئة')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_profiles.company', verbose_name='الشركة')),
            ],
            options={
                'verbose_name': 'منتج',
                'verbose_name_plural': 'المنتجات',
                'ordering': ['-created_at'],
            },
        ),
    ]
