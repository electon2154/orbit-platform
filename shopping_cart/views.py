from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from .cart import Cart
from product_catalog.models import Product

# Create your views here.

@login_required
def cart_detail(request):
    if request.user.user_type != 'customer':
        messages.error(request, 'عذراً، هذه الخدمة متاحة للمتاجر فقط')
        return redirect('home')
    cart = Cart(request)
    return render(request, 'shopping_cart/cart_detail_materio.html', {'cart': cart})

@login_required
@csrf_protect
def cart_add(request, product_id):
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'عذراً، هذه الخدمة متاحة للمتاجر فقط'})
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return JsonResponse({'success': True, 'message': 'تمت إضافة المنتج إلى السلة بنجاح'})

@login_required
@csrf_protect
def cart_remove(request, product_id):
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'عذراً، هذه الخدمة متاحة للمتاجر فقط'})
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True, 'message': 'تمت إزالة المنتج من السلة بنجاح'})

@login_required
@csrf_protect
def cart_update(request, product_id):
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'عذراً، هذه الخدمة متاحة للمتاجر فقط'})
        
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({
            'success': False,
            'message': 'بيانات غير صالحة'
        }, status=400)

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.update(product=product, quantity=quantity)
    return JsonResponse({'success': True, 'message': 'تم تحديث كمية المنتج بنجاح'})

@login_required
@csrf_protect
def cart_clear(request):
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'عذراً، هذه الخدمة متاحة للمتاجر فقط'})
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'success': True, 'message': 'تم تفريغ السلة بنجاح'})

@login_required
def cart_count(request):
    """Return the number of items in the cart as JSON."""
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'count': 0})
    
    cart = Cart(request)
    return JsonResponse({'success': True, 'count': len(cart)})
