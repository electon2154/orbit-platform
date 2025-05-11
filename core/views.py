from django.shortcuts import render
from product_catalog.models import Product
from company_profiles.models import Company
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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