from .carts import Cart

def cart(request):
    cart = Cart(request)
    if len(cart.cart.keys()) < 1:
        try:
            del cart.session[cart.coupon_id]
        except:
            ...
    return {'cart': Cart(request)}

def cart_amount(request):
    items = Cart(request)
    
    sub_total = 0
    shipping = 10
    for item in items:
        sub_total += item['sub_total']
    grand = sub_total + shipping
    return {'cart_amount': sub_total, 'grand_total': grand, 'shipping': shipping}