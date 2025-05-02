from decimal import Decimal
from django.conf import settings
from product_catalog.models import Product
from company_profiles.models import Company

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Ensure all items have total_price
        self._ensure_total_prices()

    def _ensure_total_prices(self):
        """Ensure all cart items have a total_price calculated"""
        modified = False
        for item in self.cart.values():
            if 'total_price' not in item or not item['total_price']:
                item['total_price'] = str(Decimal(item['price']) * item['quantity'])
                modified = True
        if modified:
            self.save()

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product': product.id,
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'image': product.image.url if product.image else None,
                'company_id': product.company.id,
                'company_name': product.company.name,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        # Update total_price in the cart item
        self.cart[product_id]['total_price'] = str(
            Decimal(self.cart[product_id]['price']) * self.cart[product_id]['quantity']
        )
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['total_price'] = str(
                Decimal(self.cart[product_id]['price']) * quantity
            )
            self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        # Create a mapping of product IDs to products
        product_map = {str(p.id): p for p in products}
        
        for item_id, item in cart.items():
            cart_item = item.copy()  # Create a copy to avoid modifying session data
            if item_id in product_map:
                cart_item['product_obj'] = product_map[item_id]  # Add product object for template rendering
                yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        self._ensure_total_prices()  # Ensure all items have total_price before calculating
        return sum(
            Decimal(item['total_price']) for item in self.cart.values()
        )
        
    def get_items_by_company(self):
        """
        Group cart items by company
        Returns a dictionary of company_id -> {company_name, items, total}
        """
        companies = {}
        
        # Fetch all products to get company info
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).select_related('company')
        product_map = {str(p.id): p for p in products}
        
        for item_id, item in self.cart.items():
            product = product_map.get(item_id)
            if not product:
                continue
                
            company_id = product.company.id
            
            if company_id not in companies:
                companies[company_id] = {
                    'company_name': product.company.name,
                    'items': [],
                    'total': Decimal('0')
                }
            
            # Add item to this company's items
            cart_item = item.copy()
            cart_item['product_obj'] = product
            companies[company_id]['items'].append(cart_item)
            
            # Add to company total
            companies[company_id]['total'] += Decimal(item['total_price'])
            
        return companies