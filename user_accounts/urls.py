from django.urls import path
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
    path('dashboard/company/', views.company_dashboard, name='company_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Password Management
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='user_accounts/password_change.html',
        form_class=CustomPasswordChangeForm,
        success_url='/accounts/password_change/done/'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user_accounts/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user_accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('delete-account/', views.delete_account, name='delete_account'),
] 