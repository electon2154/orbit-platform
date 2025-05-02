from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company
from .forms import CompanyForm

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_profiles/company_list.html', {'companies': companies})

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'company_profiles/company_detail.html', {'company': company})

@login_required
def company_create(request):
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
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'تم حذف الشركة بنجاح.')
        return redirect('company_profiles:company_list')
    return render(request, 'company_profiles/company_confirm_delete.html', {'company': company})
