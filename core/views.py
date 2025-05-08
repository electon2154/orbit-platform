from django.shortcuts import render
from product_catalog.models import Product
from company_profiles.models import Company

def home(request):
    # Get latest 8 products
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    # Get 6 featured companies (we can use the most recent ones for now)
    featured_companies = Company.objects.all().order_by('-id')[:6]
    
    context = {
        'latest_products': latest_products,
        'featured_companies': featured_companies,
    }
    
    # Use the new Materio template
    return render(request, 'home_materio.html', context) 