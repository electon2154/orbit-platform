from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_countries.fields import CountryField
from location_field.models.plain import PlainLocationField
from product_catalog.models import ProductCategory

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', _('Admin')),
        ('company', _('Company')),
        ('customer', _('Customer')),
        ('guest', _('Guest')),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='guest',
        verbose_name=_('User Type')
    )
    phone_number = models.CharField(max_length=20, blank=True, verbose_name=_('Phone Number'))
    email = models.EmailField(_('Email Address'), unique=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

class CompanyProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='company_profile',
        verbose_name=_('User')
    )
    company_name = models.CharField(max_length=100, verbose_name=_('Company Name'))
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('صنف الشركة')
    )
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    bio = models.TextField(blank=True, verbose_name=_('Bio'))
    logo = models.ImageField(upload_to='company_logos/', verbose_name=_('Logo'))
    baner = models.ImageField(upload_to='company_baners/', verbose_name=_('Baner'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    
    class Meta:
        verbose_name = _('Company Profile')
        verbose_name_plural = _('Company Profiles')
    
    def __str__(self):
        return self.company_name

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        verbose_name=_('User')
    )
    store_name = models.CharField(max_length=100, verbose_name=_('اسم المتجر'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))
    bio = models.TextField(blank=True, verbose_name=_('Bio'))
    logo = models.ImageField(upload_to='store_logos/', blank=True, verbose_name=_('Logo'))
    
    class Meta:
        verbose_name = _('Customer Profile')
        verbose_name_plural = _('Customer Profiles')
    
    def __str__(self):
        return self.store_name

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    store_name = models.CharField(max_length=100, verbose_name='اسم المتجر')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    address = models.TextField(verbose_name='العنوان')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    country = CountryField(verbose_name='البلد')
    location = models.CharField(max_length=255, blank=True, verbose_name='الموقع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        verbose_name = 'متجر'
        verbose_name_plural = 'المتاجر'
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name
