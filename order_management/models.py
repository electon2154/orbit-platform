from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from user_accounts.models import Customer
from product_catalog.models import Product
from core.utils import BaghdadTimestampMixin

class Order(models.Model, BaghdadTimestampMixin):
    STATUS_CHOICES = (
        ('pending', 'بانتظار الموافقة'),
        ('accepted', 'تم قبول الطلب'),
        ('processing', 'قيد التجهيز'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('rejected', 'مرفوض'),
        ('cancelled', 'ملغي'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='المتجر')
    
    # Store Information
    store_name = models.CharField(_('اسم المتجر'), max_length=255)
    store_location = models.CharField(_('موقع المتجر'), max_length=100)
    store_city = models.CharField(_('مدينة المتجر'), max_length=100)
    store_phone = models.CharField(_('هاتف المتجر'), max_length=20)
    
    order_number = models.CharField(max_length=20, unique=True, verbose_name='رقم الطلب')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='الحالة')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع الفرعي')
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الضريبة')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع النهائي')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.order_number}'

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def status_color(self):
        status_colors = {
            'pending': 'warning',
            'accepted': 'info',
            'processing': 'primary',
            'shipped': 'info',
            'delivered': 'success',
            'rejected': 'danger',
            'cancelled': 'danger'
        }
        return status_colors.get(self.status, 'secondary')

    def calculate_total(self):
        total = Decimal('0')
        for item in self.items.all():
            total += item.total
        self.total = total
        self.save()

    def can_update_status(self, user, new_status):
        if user.user_type == 'company':
            # الشركة يمكنها فقط قبول الطلب وتجهيزه وشحنه
            allowed_transitions = {
                'pending': ['accepted', 'rejected'],
                'accepted': ['processing'],
                'processing': ['shipped'],
            }
        elif user.user_type == 'customer':
            # المتجر يمكنه فقط تأكيد التسليم أو إلغاء الطلب بعد الشحن
            allowed_transitions = {
                'shipped': ['delivered', 'rejected']
            }
        else:
            return False

        current_status = self.status
        return current_status in allowed_transitions and new_status in allowed_transitions[current_status]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='الطلب')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='المنتج')
    quantity = models.PositiveIntegerField(verbose_name='الكمية')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع')

    class Meta:
        verbose_name = 'عنصر طلب'
        verbose_name_plural = 'عناصر الطلب'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.calculate_total()
