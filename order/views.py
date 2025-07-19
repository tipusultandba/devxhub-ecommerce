import uuid
import json
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import FormView
from django.db.models import Q
from .forms import CheckoutForm
from cart.carts import Cart
from cart.models import Coupon
from .models import OrderItem, Order, StatusOptions
from product.models import Product

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
class CheckoutView(generic.View):
    title = "Checkout Form"
    form_class = CheckoutForm
    template_name = 'eshop/checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        first_name = self.request.user.first_name
        last_name = self.request.user.last_name
        email = self.request.user.email
        street = self.request.user.userprofile.street
        city = self.request.user.userprofile.city
        address = self.request.user.userprofile.billing_address
        phone_no = self.request.user.userprofile.phone_number
        form = self.form_class(initial={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'street': street,
                    'city': city,
                    'address': address,
                    'phone_no': phone_no,
                })
        context = {
            'form': form,
            'title': self.title,
        }
        return render(request, self.template_name, context)
    

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return JsonResponse({
                'success': True,
                'errors': None
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            })


class SaveOrderData(generic.View):
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        cart = Cart(self.request)
        coupon_id = cart.coupon
        user_cart = Cart(self.request).cart
        products = Product.objects.filter(id__in=list(user_cart))
        ordered_products = []

        for product in products:
            order_item = OrderItem.objects.create(
                product = product,
                price = user_cart[str(product.id)]['sub_total'],
                quantity = user_cart[str(product.id)]['quantity'],
            )
            ordered_products.append(order_item)
            # update product stock.
            product.stock -= user_cart[str(product.id)]['quantity']
            product.save()

        order = Order.objects.create(
            user = self.request.user,
            discount_amount = round(cart.get_discount_amount(), 2),
            shipping_charge = round(user_cart[str(product.id)]['shipping'], 2),
            transaction_id = uuid.uuid4().hex,
            status = StatusOptions.RECEIVED,
            paypal_transaction_id = data['paypal_transaction_id'],
            total_amount = cart.grand_total(),
            paid_amount = data['amount'],
        )
        if coupon_id:
            order.coupon = Coupon.objects.get(id=coupon_id)

        order.order_items.add(*ordered_products)
        if float('%.2f' % cart.grand_total()) != float(data['amount']):
            order.paid= False
            order.save()
        order.save()
        cart.clear()
        return JsonResponse({
            'success': True,
            'errors': None
        })


class OrderListView(generic.ListView):
    permission_required = 'product.view_product'
    model = Order
    context_object_name = 'items'
    paginate_by = 10
    template_name = 'eshop/order_list.html'
    queryset = Order.objects.all()
    search_fields = ['transaction_id',]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(user=self.request.user))
        # product search start from here.
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_count'] = self.get_queryset().count()
        return context


class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = 'instance'
    pk_url_kwarg = 'pk'
    template_name = 'eshop/order_detail.html'
    title = "Payment Invoice"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
