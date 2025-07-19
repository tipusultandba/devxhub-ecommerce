from django.urls import path
from .views import AddToCard, ShopingCartListView, AddCoupon

urlpatterns = [
    path('shopping-cart/', ShopingCartListView.as_view(), name='shoping_cart'),
    path('add-cart/<int:product_id>', AddToCard.as_view(), name='add_to_cart'),
    path('add-coupon', AddCoupon.as_view(), name='add_coupon'),
]
