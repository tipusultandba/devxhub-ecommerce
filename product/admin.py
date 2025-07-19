from django.contrib import admin
from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('title', 'price', 'stock', 'in_stock', 'product_image')
    search_fields = ('title', )