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
from product_catalog.models import Product
from django.db import models
from order_management.models import Order
from django.db.models import Q
from product_catalog.models import Category

class CustomLoginView(LoginView):
    template_name = 'user_accounts/login_materio.html'

    def get_success_url(self):
        # Redirect to appropriate dashboard based on user type
        if self.request.user.user_type == 'company':
            return reverse_lazy('user_accounts:company_dashboard')
        elif self.request.user.user_type == 'customer':
            return reverse_lazy('user_accounts:browse_companies')
        elif self.request.user.is_superuser:
            return reverse_lazy('user_accounts:admin_dashboard')
        return reverse_lazy('home')

def register(request):
    if request.method == 'POST':
        print("=== Registration POST Data ===")
        print(request.POST)
        print("=== Registration FILES Data ===")
        print(request.FILES)
        
        form = RegistrationForm(request.POST, request.FILES)
        
        # Print form before validation
        print("=== Form fields before validation ===")
        for field_name, field in form.fields.items():
            print(f"{field_name}: required={field.required}, initial={field.initial}")
        
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
            print("=== Form validation errors ===")
            print(form.errors)
            print("=== Form cleaned data ===")
            print(form.cleaned_data)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    
    # Use the step-based registration template instead of register_materio.html
    return render(request, 'user_accounts/register_step_materio.html', {'form': form})

class CompanyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = 'user_accounts/company_profile_update_materio.html'
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
    template_name = 'user_accounts/customer_profile_update_materio.html'
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
    
    # Get all orders
    all_orders = Order.objects.filter(id__in=order_ids)
    total_orders = all_orders.count()
    
    # Get orders by status
    delivered_orders = all_orders.filter(status='delivered').count()
    pending_orders = all_orders.filter(status='pending').count()
    processing_orders = all_orders.filter(status='processing').count()
    cancelled_orders = all_orders.filter(status='cancelled').count()
    
    # Calculate total revenue from delivered orders
    total_revenue = all_orders.filter(status='delivered').aggregate(
        total=models.Sum('total')
    )['total'] or 0
    
    # Get recent orders
    recent_orders = all_orders.order_by('-created_at')[:5]
    
    context = {
        'company': company,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'cancelled_orders': cancelled_orders,
    }
    return render(request, 'user_accounts/company_dashboard_materio.html', context)

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
    return render(request, 'user_accounts/customer_dashboard_materio.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    # Get user statistics
    from .models import CustomUser
    total_users = CustomUser.objects.count()
    total_companies = CustomUser.objects.filter(user_type='company').count()
    total_customers = CustomUser.objects.filter(user_type='customer').count()
    recent_users = CustomUser.objects.all().order_by('-date_joined')[:5]
    
    # Get product statistics
    from product_catalog.models import Product
    total_products = Product.objects.count()
    
    # Get order statistics
    from order_management.models import Order
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='delivered').count()
    processing_orders = Order.objects.filter(status__in=['pending', 'processing', 'shipped']).count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Calculate percentages for progress bars
    if total_orders > 0:
        completed_orders_percentage = int((completed_orders / total_orders) * 100)
        processing_orders_percentage = int((processing_orders / total_orders) * 100)
        cancelled_orders_percentage = int((cancelled_orders / total_orders) * 100)
    else:
        completed_orders_percentage = 0
        processing_orders_percentage = 0
        cancelled_orders_percentage = 0
    
    # Get company statistics
    from company_profiles.models import Company
    active_companies = Company.objects.filter(is_active=True).count()
    if total_companies > 0:
        active_companies_percentage = int((active_companies / total_companies) * 100)
    else:
        active_companies_percentage = 0
    
    context = {
        'total_users': total_users,
        'total_companies': total_companies,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'recent_users': recent_users,
        'recent_orders': recent_orders,
        'completed_orders': completed_orders,
        'processing_orders': processing_orders,
        'cancelled_orders': cancelled_orders,
        'completed_orders_percentage': completed_orders_percentage,
        'processing_orders_percentage': processing_orders_percentage,
        'cancelled_orders_percentage': cancelled_orders_percentage,
        'active_companies': active_companies,
        'active_companies_percentage': active_companies_percentage,
    }
    
    return render(request, 'user_accounts/admin_dashboard_materio.html', context)

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

# Browse companies and products
@login_required
def browse_products(request):
    """View for customers to browse available products"""
    # Only customers should access this page
    if request.user.user_type == 'company':
        messages.error(request, _('هذه الصفحة متاحة فقط لحسابات المتاجر.'))
        return redirect('home')
    
    # Get all products with related data
    products = Product.objects.select_related('company', 'category').all()
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Get all categories for filtering
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'user_accounts/product_browse.html', context)



@login_required
def browse_companies(request):
    """View for customers to browse available companies"""
    # Only customers should access this page
    if request.user.user_type == 'company':
        messages.error(request, _('هذه الصفحة متاحة فقط لحسابات المتاجر.'))
        return redirect('home')
    
    # Get all companies with related data
    companies = CompanyProfile.objects.select_related('user', 'category').all()
    products = []
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        companies = companies.filter(category_id=category_id)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        products = products.order_by('-price')[:10]
        companies = companies.filter(
            Q(company_name__icontains=search_query) | 
            Q(bio__icontains=search_query)
        )
    
    # Get all categories for filtering
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'companies': companies,
        'categories': categories,
    }
    
    return render(request, 'user_accounts/company_browse.html', context)

# API endpoint for company search and products
def search_companies(request):
    """API endpoint for searching companies with suggestions"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in company names and descriptions
    companies = CompanyProfile.objects.filter(
        Q(company_name__icontains=query) | 
        Q(bio__icontains=query)
    ).select_related('category', 'user')[:10]  # Limit to 10 results
    
    # Format results for JSON response
    results = []
    for company in companies:
        logo_url = None
        if company.logo and hasattr(company.logo, 'url'):
            logo_url = company.logo.url
        
        category_name = ''
        if hasattr(company, 'category') and company.category:
            category_name = company.category.name
            
        results.append({
            'id': company.user.id,
            'name': company.company_name,
            'logo': logo_url,
            'category_name': category_name,
            'bio': company.bio[:100] if company.bio else '',
        })
    
    return JsonResponse(results, safe=False)

# API endpoint for products search
def search_products(request):
    """API endpoint for searching products with suggestions"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Search in product names and descriptions
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    ).select_related('company', 'category')[:10]  # Limit to 10 results
    
    # Format results for JSON response
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'image': product.image.url if product.image else '/static/images/default-product.png',
            'description': product.description[:100] if product.description else '',
            'company_name': product.company.name,
            'category_name': product.category.name,
        })
    
    return JsonResponse(results, safe=False)

# API endpoint for products and companies search
def search_products_and_companies(request):
    """API endpoint for searching products and companies with suggestions"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
        
    # Search in product and company names and descriptions
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    ).select_related('company', 'category')[:10]  # Limit to 10 results
    
    companies = CompanyProfile.objects.filter(
        Q(company_name__icontains=query) | 
        Q(bio__icontains=query)
    ).select_related('category', 'user')[:10]  # Limit to 10 results

    # Format results for JSON response
    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'description': product.description[:100] if product.description else '',
            'company_name': product.company.name,
            'category_name': product.category.name,
        })

    for company in companies:
        results.append({
            'id': company.user.id,
            'name': company.company_name,
            'logo': company.logo.url if company.logo else '/static/images/default-company.png',
            'category_name': company.category.name,
        })
    
    # Get all categories for filtering
    categories = Category.objects.all()
    
    context = {
        'companies': companies,
        'categories': categories,
    }
    
    return render(request, 'user_accounts/company_browse.html', context)
