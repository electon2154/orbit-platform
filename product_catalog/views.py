from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Product, Category, ProductCategory
from .forms import ProductForm
from user_accounts.models import CompanyProfile, CustomUser
from company_profiles.models import Company
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models import Q

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
    search_query = request.GET.get('q')
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
    # Use the new Materio-themed template
    return render(request, 'product_catalog/product_list_materio.html', context)

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
    # Use the new Materio-themed template
    return render(request, 'product_catalog/product_form_materio.html', {'form': form, 'action': 'إنشاء'})

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
    # Use the new Materio-themed template
    return render(request, 'product_catalog/product_form_materio.html', {'form': form, 'action': 'تحديث'})

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

@login_required
def company_products(request, company_id):
    """Display products from a specific company"""
    try:
        # Use the CustomUser model instead of User
        company_user = CustomUser.objects.get(id=company_id, user_type='company')
        company = CompanyProfile.objects.get(user=company_user)
    except (CustomUser.DoesNotExist, CompanyProfile.DoesNotExist):
        messages.error(request, _('الشركة غير موجودة'))
        return redirect('user_accounts:browse_companies')
    
    # Get company's products - find the company object first
    try:
        company_obj = Company.objects.get(name=company.company_name)
        products = Product.objects.filter(company=company_obj, is_active=True).order_by('-created_at')
    except Company.DoesNotExist:
        products = []
        company_obj = None
    
    # Handle search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Handle category filtering
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Get categories for filtering
    categories = Category.objects.all()
    
    context = {
        'company': company,
        'company_obj': company_obj,  # Pass the actual Company object for API calls
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'product_catalog/company_products.html', context)

# API endpoint for company product search
def search_company_products(request):
    """API endpoint for searching products within a specific company with suggestions"""
    query = request.GET.get('q', '')
    company_id = request.GET.get('company_id')
    
    if len(query) < 2 or not company_id:
        return JsonResponse([], safe=False)
    
    try:
        # Log for debugging
        print(f"Searching for products with query: '{query}' in company ID: {company_id}")
        
        # Get the company
        company_obj = get_object_or_404(Company, id=company_id)
        print(f"Found company: {company_obj.name}")
        
        # Search products by name and description for this company
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            company=company_obj,
            is_active=True
        )[:10]  # Limit to 10 results
        
        print(f"Found {products.count()} matching products")
        
        # Format results for JSON response
        results = []
        for product in products:
            image_url = None
            if product.image and hasattr(product.image, 'url'):
                image_url = product.image.url
                
            results.append({
                'id': product.id,
                'name': product.name,
                'image': image_url or '/static/images/default-product.png',
                'price': float(product.price),
                'category': product.category.name if product.category else '',
                'description': product.description[:100] if product.description else '',
            })
        
        return JsonResponse(results, safe=False)
    except Exception as e:
        print(f"Error in search_company_products: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
