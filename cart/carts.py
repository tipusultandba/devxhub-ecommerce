from django.conf import settings 
from product.models import Product
from .models import Coupon


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.cart_id = settings.CART_ID
        self.coupon_id = settings.COUPON_ID
        cart = self.session.get(self.cart_id)
        coupon = self.session.get(self.coupon_id)
        self.cart = self.session[self.cart_id] = cart if cart else {}
        self.coupon = self.session[self.coupon_id] = coupon if coupon else None

    def update(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        self.session[self.cart_id].setdefault(str(product_id), {'quantity': 0})
        updated_quantity = self.session[self.cart_id][str(product_id)]['quantity'] + quantity
        self.session[self.cart_id][str(product_id)]['quantity'] = updated_quantity
        self.session[self.cart_id][str(product_id)]['sub_total'] = updated_quantity * float(product.price)
        self.session[self.cart_id][str(product_id)]['shipping'] = 10

        if updated_quantity < 1:
            del self.session[self.cart_id][str(product_id)]
        
        self.save()

    def add_coupon(self, coupon_id):
        self.session[self.coupon_id] = coupon_id
        self.save()

    def __iter__(self):
        products = Product.objects.filter(id__in=list(self.cart.keys()))
        cart = self.cart.copy()

        for item in products:
            product = Product.objects.get(id=item.id)
            cart[str(item.id)]['product'] = {
                "id": item.id,
                "title": item.title,
                "price": float(item.price),
                "thumbnail": f'/media/{item.thumbnail}',
                "slug": item.slug,
            }
            yield cart[str(item.id)]

    def save(self):
        self.session.modified = True
    
    def __len__(self):
        return len(list(self.cart.keys()))
    
    def clear(self):
        try:
            del self.session[self.cart_id]
            del self.session[self.coupon_id]
        except:
            pass
        self.save()
    
    def restore_after_logout(self, current_cart={}, current_coupon=None):
        self.cart = self.session[self.cart_id]=current_cart
        self.coupon = self.session[self.coupon_id]=current_coupon
        self.save()

    def actual_total(self):
        amount = sum(product['sub_total'] for product in self.cart.values())
        return amount
    
    def total_discount(self):
        amount = sum(product['sub_total'] for product in self.cart.values())
        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            if self.actual_total() > coupon.required_amount_use_coupon:
                discount = amount * (coupon.discount / 100)
                return discount
            else:
                return 0
        else:
            return None
    
    def grand_total(self):
        amount = sum(product['sub_total'] for product in self.cart.values())
        shipping = 10
        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            if self.actual_total() > coupon.required_amount_use_coupon:
                amount -= amount * (coupon.discount / 100)
        return amount + shipping
    
    def get_discount_amount(self):
        amount = sum(product['sub_total'] for product in self.cart.values())
        shipping = 10
        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            if self.actual_total() > coupon.required_amount_use_coupon:
                discount = amount * (coupon.discount / 100)
        return discount