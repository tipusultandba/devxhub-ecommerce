from django.db import models 
from product.models import Product
from cart.models import Coupon
from django.contrib.auth import get_user_model
User = get_user_model()


class StatusOptions(models.TextChoices):
    """ CONSTANT = DB_VALUE, USER_DISPLAY_VALUE  """
    RECEIVED = 'received', 'Received'
    ON_WAY = 'on the way', 'On The Way'
    DELIVERED = 'delivered', 'Delivered'


# Create your models here.
class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete = models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=True)
    transaction_id = models.UUIDField()
    paypal_transaction_id = models.CharField(max_length=30)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=15, choices=StatusOptions.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='updated_%(class)ss', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
