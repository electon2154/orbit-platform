from django.contrib import admin
from .models import Product, Category, ProductCategory

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'stock', 'category', 'company', 'is_active')
    list_filter = ('category', 'company', 'is_active')
    search_fields = ('name', 'code', 'description')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)
