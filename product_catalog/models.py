from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from core.utils import BaghdadTimestampMixin

class Category(models.Model, BaghdadTimestampMixin):
    name = models.CharField(max_length=255, verbose_name='اسم الفئة')
    description = models.TextField(blank=True, verbose_name='الوصف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model, BaghdadTimestampMixin):
    name = models.CharField(max_length=255, verbose_name='اسم المنتج')
    code = models.CharField(max_length=50, blank=True, auto_created=True, verbose_name='رمز المنتج')
    description = RichTextField(verbose_name='الوصف')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    stock = models.PositiveIntegerField(default=0, verbose_name='المخزون')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='الصورة')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='الفئة')
    company = models.ForeignKey('company_profiles.Company', on_delete=models.CASCADE, verbose_name='الشركة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductCategory(models.Model, BaghdadTimestampMixin):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم الفئة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الفئة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "فئة المنتجات"
        verbose_name_plural = "فئات المنتجات"
        ordering = ['name']

    def __str__(self):
        return self.name
