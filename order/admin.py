import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import (Order, OrderItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'paid', 'transaction_id', 'status', 'created_at')
    search_fields = ('transaction_id', 'order_items')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()
    
    
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'quantity')
    search_fields = ('product__title',)
