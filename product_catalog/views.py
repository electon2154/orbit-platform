from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Product, Category, ProductCategory
from .forms import ProductForm
from user_accounts.models import CompanyProfile
from company_profiles.models import Company
from django.http import JsonResponse

def product_list(request):
    # Filter products based on user type
    if request.user.is_authenticated and request.user.user_type == 'company':
        # Get company profile and show only their products
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
        company = get_object_or_404(Company, name=company_profile.company_name)
        products = Product.objects.filter(company=company, is_active=True)
    else:
        # For customers and anonymous users, show all active products
        products = Product.objects.filter(is_active=True)
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by company if specified
    company_id = request.GET.get('company')
    if company_id and request.user.user_type != 'company':
        products = products.filter(company_id=company_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    # Get all categories for the filter
    categories = Category.objects.all()
    
    # Get all companies for the filter (only for customer view)
    companies = None
    if request.user.is_authenticated and request.user.user_type != 'company':
        companies = Company.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'companies': companies,
    }
    return render(request, 'product_catalog/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_catalog/product_detail.html', context)

@login_required
def product_create(request):
    # Check if the user is a company
    if request.user.user_type != 'company':
        messages.error(request, 'عذراً، فقط الشركات يمكنها إضافة منتجات جديدة.')
        return redirect('product_catalog:product_list')
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Get the company profile of the current user
            company_profile = get_object_or_404(CompanyProfile, user=request.user)
            
            # Get the company instance directly
            company = get_object_or_404(Company, name=company_profile.company_name)
            
            # Get or create the default category
            default_category, created = Category.objects.get_or_create(
                name="غذائية",
                defaults={
                    'description': "المنتجات الغذائية"
                }
            )
            
            # Set the company, category and is_active
            product.company = company
            product.category = default_category
            product.is_active = True
            
            product.save()
            messages.success(request, 'تم إضافة المنتج بنجاح.')
            return redirect('user_accounts:company_dashboard')
    else:
        form = ProductForm()
    return render(request, 'product_catalog/product_form.html', {'form': form, 'action': 'إنشاء'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Check if the user owns this product
    if request.user.user_type != 'company':
        messages.error(request, 'عذراً، لا يمكنك تعديل هذا المنتج.')
        return redirect('product_catalog:product_list')
        
    company_profile = get_object_or_404(CompanyProfile, user=request.user)
    company = get_object_or_404(Company, name=company_profile.company_name)
    
    if product.company != company:
        messages.error(request, 'عذراً، لا يمكنك تعديل هذا المنتج.')
        return redirect('product_catalog:product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'تم تحديث المنتج بنجاح.')
            return redirect('product_catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_catalog/product_form.html', {'form': form, 'action': 'تحديث'})

@login_required
def product_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'طريقة الطلب غير صحيحة'}, status=405)
    
    try:
        product = get_object_or_404(Product, pk=pk)
        
        # Check if the user owns this product
        if request.user.user_type != 'company':
            return JsonResponse({'success': False, 'message': 'عذراً، لا يمكنك حذف هذا المنتج'}, status=403)
            
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
        company = get_object_or_404(Company, name=company_profile.company_name)
        
        if product.company != company:
            return JsonResponse({'success': False, 'message': 'عذراً، لا يمكنك حذف هذا المنتج'}, status=403)
        
        # Delete the product
        product.delete()
        return JsonResponse({'success': True, 'message': 'تم حذف المنتج بنجاح'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
