from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import datetime
from .models import Company
from .forms import CompanyForm
from order_management.models import Order, OrderItem
from product_catalog.models import Product

def company_list(request):
    if request.user.is_authenticated == False or request.user.user_type != 'admin':
        return redirect('home')
    companies = Company.objects.all()
    print(companies.all)
    return render(request, 'company_profiles/company_list.html', {'companies': companies})

def company_detail(request, pk):
    if request.user.is_authenticated == False or request.user.user_type != 'admin':
        return redirect('home')
    company = get_object_or_404(Company, pk=pk)
    
    # Get products for this company
    company_products = Product.objects.filter(company=company)
    
    # Get all orders that contain any of this company's products
    order_items = OrderItem.objects.filter(product__in=company_products)
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
    
    # Filter by status if specified
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Filter by date range if specified
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        try:
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            # Add one day to end_date to include the end date in the results
            end_date_obj = end_date_obj + datetime.timedelta(days=1)
            
            orders = orders.filter(
                created_at__gte=start_date_obj,
                created_at__lt=end_date_obj
            )
        except ValueError:
            # Invalid date format, ignore the filter
            pass
    
    # Paginate the orders
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        'company': company,
        'orders': orders,
        'status': status,
        'start_date': start_date,
        'end_date': end_date
    }
    
    return render(request, 'company_profiles/company_detail.html', context)

@login_required
def company_create(request):
    if request.user.is_authenticated == False or request.user.user_type != 'admin':
        return redirect('home')
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            messages.success(request, 'تم إنشاء الشركة بنجاح.')
            return redirect('company_profiles:company_detail', pk=company.pk)
    else:
        form = CompanyForm()
    return render(request, 'company_profiles/company_form.html', {'form': form, 'action': 'إنشاء'})

@login_required
def company_update(request, pk):
    if request.user.is_authenticated == False or request.user.user_type != 'admin':
        return redirect('home')
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save()
            messages.success(request, 'تم تحديث الشركة بنجاح.')
            return redirect('company_profiles:company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'company_profiles/company_form.html', {'form': form, 'action': 'تحديث'})

@login_required
def company_delete(request, pk):
    if request.user.is_authenticated == False or request.user.user_type != 'admin':
        return redirect('home')
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'تم حذف الشركة بنجاح.')
        return redirect('company_profiles:company_list')
    return render(request, 'company_profiles/company_confirm_delete.html', {'company': company})
