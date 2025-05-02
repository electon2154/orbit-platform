from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, DetailView
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, CompanyProfileForm, CustomerProfileForm
from .models import CustomUser, CompanyProfile, CustomerProfile, Customer
from company_profiles.models import Company
from django.db import models
from order_management.models import Order

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'company':
            return reverse_lazy('user_accounts:company_dashboard')
        elif user.user_type == 'customer':
            return reverse_lazy('user_accounts:customer_dashboard')
        elif user.is_superuser:
            return reverse_lazy('user_accounts:admin_dashboard')
        return reverse_lazy('home')

def register(request):
    if request.method == 'POST':
        print("registeration POST")
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, _('تم التسجيل بنجاح!'))
                login(request, user)

                # Redirect based on user type
                if user.user_type == 'company':
                    return redirect('user_accounts:company_dashboard')
                elif user.user_type == 'customer':
                    return redirect('user_accounts:customer_dashboard')
                else:
                    return redirect('home')
            except Exception as e:
                messages.error(request, _('حدث خطأ أثناء التسجيل. يرجى المحاولة مرة أخرى.'))
                print(f"Registration error: {str(e)}")  # For debugging
                print(f"Form data: {form.cleaned_data}")  # For debugging
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            print(f"Form errors: {form.errors}")  # For debugging
    else:
        form = RegistrationForm()
    
    return render(request, 'user_accounts/register.html', {'form': form})

class CompanyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = 'user_accounts/company_profile_update.html'
    success_url = reverse_lazy('user_accounts:company_dashboard')

    def get_object(self):
        return get_object_or_404(CompanyProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث الملف الشخصي بنجاح'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('حدث خطأ أثناء تحديث الملف الشخصي'))
        return super().form_invalid(form)

class CustomerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerProfileForm
    template_name = 'user_accounts/customer_profile_update.html'
    success_url = reverse_lazy('user_accounts:customer_dashboard')

    def get_object(self):
        return get_object_or_404(Customer, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث الملف الشخصي بنجاح'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('حدث خطأ أثناء تحديث الملف الشخصي'))
        return super().form_invalid(form)

class CompanyProfileDetailView(DetailView):
    model = CompanyProfile
    template_name = 'user_accounts/company_profile_detail.html'
    context_object_name = 'profile'

class CustomerProfileDetailView(DetailView):
    model = CustomerProfile
    template_name = 'user_accounts/customer_profile_detail.html'
    context_object_name = 'profile'

@login_required
def company_dashboard(request):
    if not request.user.user_type == 'company':
        return redirect('home')
    
    company_profile = get_object_or_404(CompanyProfile, user=request.user)
    
    # Get or create the Company instance
    from company_profiles.models import Company
    company, created = Company.objects.get_or_create(
        name=company_profile.company_name,
        defaults={
            'email': request.user.email,
            'phone': request.user.phone_number,
            'address': company_profile.location,
            'city': company_profile.city,
            'description': company_profile.bio or '',
            'logo': company_profile.logo
        }
    )
    
    # Get product statistics
    from product_catalog.models import Product
    total_products = Product.objects.filter(company=company).count()
    recent_products = Product.objects.filter(company=company).order_by('-created_at')[:5]
    
    # Get order statistics
    from order_management.models import Order, OrderItem
    company_products = Product.objects.filter(company=company)
    order_items = OrderItem.objects.filter(product__in=company_products)
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    total_orders = Order.objects.filter(id__in=order_ids).count()
    total_revenue = Order.objects.filter(id__in=order_ids, status='delivered').aggregate(
        total=models.Sum('total')
    )['total'] or 0
    
    # Get recent orders
    recent_orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')[:5]
    
    context = {
        'company': company,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    return render(request, 'user_accounts/company_dashboard.html', context)

@login_required
def customer_dashboard(request):
    if not request.user.user_type == 'customer':
        return redirect('home')
    
    customer = get_object_or_404(Customer, user=request.user)
    
    # Get order statistics
    orders = Order.objects.filter(customer=customer)
    total_orders = orders.count()
    total_spent = orders.filter(status='delivered').aggregate(
        total=models.Sum('total')
    )['total'] or 0
    
    # Get recent orders
    recent_orders = orders.order_by('-created_at')[:5]
    
    context = {
        'customer': customer,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
        'wishlist_count': 0,  # TODO: Implement wishlist functionality
        'wishlist_products': [],  # TODO: Implement wishlist functionality
    }
    return render(request, 'user_accounts/customer_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    return render(request, 'user_accounts/admin_dashboard.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Delete the user's profile first
        if hasattr(user, 'company_profile'):
            user.company_profile.delete()
        elif hasattr(user, 'customer_profile'):
            user.customer_profile.delete()
        # Delete the user
        user.delete()
        messages.success(request, _('تم حذف حسابك بنجاح'))
        return redirect('user_accounts:login')
    return redirect('user_accounts:company_profile_update')
