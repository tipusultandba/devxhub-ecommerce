from django.urls import path, include
from .views import CheckoutView, SaveOrderData, OrderListView, OrderDetailView


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('save-order/', SaveOrderData.as_view(), name='save_order'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-details/<int:pk>', OrderDetailView.as_view(), name='order_details'),
    
]