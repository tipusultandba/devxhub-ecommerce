from django.db import models

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=25)
    discount = models.PositiveIntegerField(help_text='Discount in percentage')
    active = models.BooleanField(default=True)
    active_date = models.DateField()
    expiry_date = models.DateField()
    required_amount_use_coupon = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.code
