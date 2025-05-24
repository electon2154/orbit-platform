from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordChangeForm

app_name = 'user_accounts'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Registration
    path('register/', views.register, name='register'),
    
    # Profile Management
    path('profile/company/', views.CompanyProfileUpdateView.as_view(), name='company_profile_update'),
    path('profile/customer/', views.CustomerProfileUpdateView.as_view(), name='customer_profile_update'),
    
    # Dashboard
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Browse companies and products
    path('browse/companies/', views.browse_companies, name='browse_companies'),
    path('browse/products/', views.browse_products, name='browse_products'),
    
    # API endpoints
    path('api/search/companies/', views.search_companies, name='search_companies'),
    path('api/search/products/', views.search_products, name='search_products'),
    path('api/search/products_and_companies/', views.search_products_and_companies, name='search_products_and_companies'),
    
    # Profile
    path('profile/update/customer/', views.CustomerProfileUpdateView.as_view(), name='customer_profile_update'),
    
    # Password Management
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='user_accounts/password_change_form.html',
        success_url=reverse_lazy('user_accounts:password_change_done')), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='user_accounts/password_change_done.html'), 
        name='password_change_done'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='user_accounts/password_reset.html',
        email_template_name='user_accounts/password_reset_email.html',
        subject_template_name='user_accounts/password_reset_subject.txt',
        success_url=reverse_lazy('user_accounts:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user_accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user_accounts/password_reset_confirm.html',
        success_url=reverse_lazy('user_accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user_accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path('delete-account/', views.delete_account, name='delete_account'),
] 