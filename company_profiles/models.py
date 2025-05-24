from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from core.utils import BaghdadTimestampMixin

class Company(models.Model, BaghdadTimestampMixin):
    name = models.CharField(max_length=255, verbose_name='اسم الشركة')
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name='الشعار')
    description = models.TextField(verbose_name='الوصف')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    address = models.TextField(verbose_name='العنوان')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name='الموقع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        verbose_name = 'شركة'
        verbose_name_plural = 'الشركات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
