from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from custom_auth.views import (SignUpCreateView, UserLoginView, UserLogoutView, UserPasswordChangeView, HomeView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    # Authentication urls.
    path('signup/', SignUpCreateView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('password-change/', UserPasswordChangeView.as_view(), name='user_password_change'),
    # User Profile usls.
    path('user-profile/', include('user_profile.urls')),
    # Products Urls
    path('products/', include('product.urls')),
    # cart urls
    path('cart/', include('cart.urls')),
    # order urls
    path('orders/', include('order.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ADMIN PANEL HEADER AND TITLE TEXT CHANGE.
admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "Welcome to E-Commerce Portal"


# Custom erorrs Page
handler404 = 'custom_auth.views.custom_page_not_found'
handler500 = 'custom_auth.views.custom_server_error'
handler403 = 'custom_auth.views.custom_permission_denied_view'
handler400 = 'custom_auth.views.custom_bad_request_view'
