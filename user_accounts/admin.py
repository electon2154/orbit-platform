from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, CompanyProfile, CustomerProfile

class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    can_delete = False
    verbose_name_plural = _('Company Profile')

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = _('Customer Profile')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.user_type == 'company':
                return [CompanyProfileInline]
            elif obj.user_type == 'customer':
                return [CustomerProfileInline]
        return []

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'city', 'website')
    search_fields = ('company_name', 'user__username', 'city')
    list_filter = ('city',)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'city')
    search_fields = ('store_name', 'user__username', 'city')
    list_filter = ('city',)
