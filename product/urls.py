from django.urls import path, include
from .views import *


urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('product-list-api/', ProductListApiView.as_view(), name='product_list_api'),
]