from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.template.loader import render_to_string
import json
from decimal import Decimal
from .models import Order, OrderItem
from .forms import OrderForm, OrderStatusForm
from shopping_cart.cart import Cart
from product_catalog.models import Product
from user_accounts.models import CompanyProfile, Customer
from company_profiles.models import Company
import uuid

@login_required
def order_list(request):
    # Show only relevant orders based on user type
    if request.user.user_type == 'customer':
        # Get the customer instance for the current user
        customer = get_object_or_404(Customer, user=request.user)
        orders = Order.objects.filter(customer=customer)
    elif request.user.user_type == 'company':
        # Get the company instance for the current user
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
        company = get_object_or_404(Company, name=company_profile.company_name)
        
        # Get products for this company
        company_products = Product.objects.filter(company=company)
        
        # Get all orders that contain any of this company's products
        order_items = OrderItem.objects.filter(product__in=company_products)
        order_ids = order_items.values_list('order_id', flat=True).distinct()
        orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')
        
    return render(request, 'order_management/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order,
        'is_company': request.user.user_type == 'company',
        'is_customer': request.user.user_type == 'customer',
    }
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Simple HTML template without the back button for AJAX
        html = """
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">تفاصيل الطلب #{{ order.order_number }}</h4>
            </div>
            <div class="card-body">
                <!-- Order Status -->
                <div class="mb-4">
                    <h6 class="mb-3">حالة الطلب</h6>
                    <span class="badge bg-{{ order.status_color }} fs-6">
                        {{ order.get_status_display }}
                    </span>
                </div>

                <!-- Order Details -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h6 class="mb-3">معلومات المتجر</h6>
                        <p><strong>اسم المتجر:</strong> {{ order.customer.store_name }}</p>
                        <p><strong>المدينة:</strong> {{ order.store_city }}</p>
                        <p><strong>رقم الهاتف:</strong> {{ order.store_phone }}</p>
                    </div>
                </div>

                <!-- Order Items -->
                <div class="table-responsive mb-4">
                    <h6 class="mb-3">المنتجات</h6>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>المنتج</th>
                                <th>الكمية</th>
                                <th>السعر</th>
                                <th>المجموع</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in order.items.all %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        {% if item.product.image %}
                                        <img src="{{ item.product.image.url }}" width="40" height="40" 
                                             class="rounded me-2" alt="{{ item.product.name }}">
                                        {% endif %}
                                        {{ item.product.name }}
                                    </div>
                                </td>
                                <td>{{ item.quantity }}</td>
                                <td>{{ item.price|floatformat:2 }} دينار عراقي</td>
                                <td>{{ item.total|floatformat:2 }} دينار عراقي</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                        <tfoot>
                            <tr>
                                <td colspan="3" class="text-end"><strong>المجموع الفرعي:</strong></td>
                                <td><strong>{{ order.subtotal|floatformat:2 }} دينار عراقي</strong></td>
                            </tr>
                            <tr>
                                <td colspan="3" class="text-end"><strong>الضريبة:</strong></td>
                                <td><strong>{{ order.tax|floatformat:2 }} دينار عراقي</strong></td>
                            </tr>
                            <tr>
                                <td colspan="3" class="text-end"><strong>المجموع النهائي:</strong></td>
                                <td><strong>{{ order.total|floatformat:2 }} دينار عراقي</strong></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>
        """
        
        # Convert the HTML template string to actual template
        from django.template import Template, Context
        template = Template(html)
        template_context = Context(context)
        rendered_html = template.render(template_context)
        
        return JsonResponse({'html': rendered_html, 'success': True})
    
    return render(request, 'order_management/order_detail.html', context)

@login_required
def order_create(request):
    if request.user.user_type != 'customer':
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': False,
                'message': 'عذراً، يمكن للمتاجر فقط إنشاء طلبات جديدة'
            }, status=403)
        messages.error(request, 'عذراً، يمكن للمتاجر فقط إنشاء طلبات جديدة')
        return redirect('home')
    
    # Redirect GET requests to create_order_for_company
    if request.method == 'GET':
        company_id = request.GET.get('company')
        if company_id:
            return redirect(f'/order-management/create-company-order/?company={company_id}')
        return redirect('shopping_cart:cart_detail')
    
    # Process POST requests as before
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
        
    try:
        customer = get_object_or_404(Customer, user=request.user)
        cart = Cart(request)
        
        # Check if cart exists and has items
        if not cart or len(cart) == 0:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'لا يمكن إنشاء طلب بسلة فارغة'
                }, status=400)
            messages.error(request, 'لا يمكن إنشاء طلب بسلة فارغة')
            return redirect('shopping_cart:cart_detail')

        # Use cart's total price which is already calculated
        subtotal = cart.get_total_price()
        
        # Create order number
        import random
        import string
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Create the order
        order = Order.objects.create(
            customer=customer,
            order_number=order_number,
            store_name=customer.store_name,
            store_location=customer.location,
            store_city=customer.city,
            store_phone=customer.phone,
            subtotal=subtotal,
            tax=Decimal('0'),  # You can modify tax calculation as needed
            total=subtotal,
            status='pending'
        )

        # Create order items and verify products exist
        try:
            for item in cart:
                product = Product.objects.get(id=item['product'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=Decimal(item['price']),
                    total=Decimal(item['total_price'])
                )
        except Product.DoesNotExist:
            # If any product doesn't exist, delete the order and return error
            order.delete()
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': f'المنتج غير موجود: {item["name"]}'
                }, status=400)
            messages.error(request, f'المنتج غير موجود: {item["name"]}')
            return redirect('shopping_cart:cart_detail')

        # Clear the cart only after successful order creation
        cart.clear()

        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': True,
                'message': 'تم إنشاء الطلب وتفريغ السلة بنجاح',
                'order_id': order.id
            }, status=201)

        messages.success(request, 'تم إنشاء الطلب وتفريغ السلة بنجاح')
        return redirect('user_accounts:customer_dashboard')

    except Exception as e:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
        messages.error(request, f'حدث خطأ أثناء إنشاء الطلب: {str(e)}')
        return redirect('shopping_cart:cart_detail')

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'تم تحديث الطلب بنجاح.')
            return redirect('order_management:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_management/order_form.html', {'form': form, 'action': 'تحديث'})

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'تم حذف الطلب بنجاح.')
        return redirect('order_management:order_list')
    return render(request, 'order_management/order_confirm_delete.html', {'order': order})

@login_required
def order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            # التحقق من صلاحية الحالة الجديدة
            if new_status not in dict(Order.STATUS_CHOICES):
                return JsonResponse({
                    'success': False, 
                    'message': 'حالة الطلب غير صالحة'
                })
            
            # التحقق من صلاحية المستخدم لتغيير الحالة
            if not order.can_update_status(request.user, new_status):
                return JsonResponse({
                    'success': False,
                    'message': 'غير مسموح لك بتغيير حالة الطلب إلى هذه الحالة'
                })

            # تحديث حالة الطلب
            order.status = new_status
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': 'تم تحديث حالة الطلب بنجاح',
                'status': order.get_status_display(),
                'status_color': order.status_color
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'بيانات غير صالحة'})
    
    return render(request, 'order_management/order_status_form.html', {
        'form': OrderStatusForm(instance=order), 
        'order': order
    })

@login_required
@ensure_csrf_cookie
def company_orders_api(request):
    """API endpoint لجلب بيانات الطلبات للخريطة"""
    if request.user.user_type != 'company':
        return JsonResponse({'error': 'غير مصرح'}, status=403)
    
    try:
        # Get the company instance for the current user
        company_profile = get_object_or_404(CompanyProfile, user=request.user)
        company = get_object_or_404(Company, name=company_profile.company_name)
        
        # Get products for this company
        company_products = Product.objects.filter(company=company)
        
        # Get all orders that contain any of this company's products
        order_items = OrderItem.objects.filter(product__in=company_products)
        order_ids = order_items.values_list('order_id', flat=True).distinct()
        orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
        
        # Prepare orders data for the map
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'store_name': order.store_name,
                'store_location': order.store_location,
                'status': order.status,
                'status_display': order.get_status_display(),
                'status_color': order.status_color,
                'total': str(order.total),
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse(orders_data, safe=False)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'message': 'حدث خطأ أثناء جلب بيانات الطلبات'
        }, status=500)

@login_required
def create_order_for_company(request):
    """Create an order for products from a specific company in the cart"""
    if request.user.user_type != 'customer':
        messages.error(request, 'عذراً، هذه الخدمة متاحة للمتاجر فقط')
        return redirect('home')
    
    company_id = request.GET.get('company')
    if not company_id:
        messages.error(request, 'لم يتم تحديد الشركة')
        return redirect('shopping_cart:cart_detail')
    
    # Get customer instance
    customer = get_object_or_404(Customer, user=request.user)
    
    # Get cart and filter items by company
    cart = Cart(request)
    company_items = {}
    
    # Get company data from cart
    companies_data = cart.get_items_by_company()
    if int(company_id) not in companies_data:
        messages.error(request, 'لا توجد منتجات من هذه الشركة في السلة')
        return redirect('shopping_cart:cart_detail')
    
    company_data = companies_data[int(company_id)]
    
    try:
        # Create order
        order = Order.objects.create(
            customer=customer,
            store_name=customer.store_name,
            store_location=customer.location,
            store_city=customer.city,
            store_phone=customer.phone,
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            status='pending',
            subtotal=company_data['total'],
            tax=Decimal('0.00'),  # No tax for now
            total=company_data['total']
        )
        
        # Create order items
        for item in company_data['items']:
            product = item['product_obj']
            OrderItem.objects.create(
                order=order,
                product=product,
                price=Decimal(item['price']),
                quantity=item['quantity']
            )
            
            # Remove items from cart
            cart.remove(product)
        
        messages.success(request, 'تم إنشاء الطلب بنجاح')
        return redirect('order_management:order_detail', pk=order.id)
        
    except Exception as e:
        messages.error(request, f'حدث خطأ أثناء إنشاء الطلب: {str(e)}')
        return redirect('shopping_cart:cart_detail')

@login_required
def create_all_orders(request):
    """Create orders for all companies in the cart"""
    if request.user.user_type != 'customer':
        messages.error(request, 'عذراً، هذه الخدمة متاحة للمتاجر فقط')
        return redirect('home')
    
    # Get customer instance
    customer = get_object_or_404(Customer, user=request.user)
    
    # Get cart and items by company
    cart = Cart(request)
    companies_data = cart.get_items_by_company()
    
    if not companies_data:
        messages.error(request, 'السلة فارغة')
        return redirect('shopping_cart:cart_detail')
    
    created_orders = []
    
    try:
        # Create orders for each company
        for company_id, company_data in companies_data.items():
            # Create order
            order = Order.objects.create(
                customer=customer,
                store_name=customer.store_name,
                store_location=customer.location,
                store_city=customer.city,
                store_phone=customer.phone,
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                status='pending',
                subtotal=company_data['total'],
                tax=Decimal('0.00'),  # No tax for now
                total=company_data['total']
            )
            
            # Create order items
            for item in company_data['items']:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=Decimal(item['price']),
                    quantity=item['quantity']
                )
                
                # Remove items from cart
                cart.remove(product)
            
            created_orders.append(order.id)
        
        # Clear the cart
        cart.clear()
        
        if len(created_orders) == 1:
            messages.success(request, 'تم إنشاء الطلب بنجاح')
            return redirect('order_management:order_detail', pk=created_orders[0])
        else:
            messages.success(request, f'تم إنشاء {len(created_orders)} طلبات بنجاح')
            return redirect('order_management:order_list')
            
    except Exception as e:
        messages.error(request, f'حدث خطأ أثناء إنشاء الطلبات: {str(e)}')
        return redirect('shopping_cart:cart_detail')
