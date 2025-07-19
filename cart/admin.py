from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'active_date', 'expiry_date', 'required_amount_use_coupon')
    search_fields = ('code',)
