from django.shortcuts import render, get_object_or_404, HttpResponseRedirect,redirect
from django.db.models import Q, Prefetch, Sum, Value
from django.views import generic
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from product.models import Product
from .carts import Cart
from .models import Coupon


def format_search_string(fields, keyword):
    Qr = None
    for field in fields:        
        q = Q(**{"%s__icontains" % field: keyword })
        if Qr:
            Qr = Qr | q
        else:
            Qr = q    
    return Qr

# Create your views here.
class AddToCard(generic.View):
    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id, 1)
        return redirect('shoping_cart')


class ShopingCartListView(generic.ListView):
    permission_required = 'eshop.view_product'
    model = Product
    context_object_name = 'items'
    paginate_by = 9
    template_name = 'eshop/cart.html'
    queryset = Product.objects.all()
    search_fields = ['title', 'category__title']
    
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        cart = Cart(self.request)
        print(cart.coupon, "Coupon")
        if product_id and quantity:
            # product = get_object_or_404(Product, pk=kwargs.get('product_id'))
            cart.update(int(product_id), int(quantity))
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            return super().get(request, *args, **kwargs)
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)

        return queryset
    

class AddCoupon(generic.View):
    def post(self, *args, **kwargs):
        code = self.request.POST.get('coupon_code')
        coupon = Coupon.objects.filter(code__iexact=code, active=True)
        cart = Cart(self.request)

        if coupon.exists():
            coupon = coupon.first()
            current_date = datetime.date(timezone.now())
            active_date = coupon.active_date
            expiry_date = coupon.expiry_date

            if current_date > expiry_date:
                messages.warning(self.request, "Coupon Expired!")
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
            
            if current_date < active_date:
                messages.warning(self.request, "Coupon is yet to be available")
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
            
            if cart.actual_total() < coupon.required_amount_use_coupon:
                messages.warning(self.request, f"Your have to shop at least ${coupon.required_amount_use_coupon} to use this coupon code!")
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

            cart.add_coupon(coupon.id)
            messages.success(self.request, "Your Coupon has been included Successfully.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            messages.warning(self.request, "Invalid Coupon Code!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))