from django.shortcuts import resolve_url, render
from django.http import Http404
from django.views import View, generic
from django.conf import settings
from .forms import *
from django.contrib.auth.models import User
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView)
from django.contrib.auth import (login as auth_login)
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
import copy
from .log_entry import CustomLogEntry
from .mixin import CommonMixin
from user_profile.models import UserProfile
from cart.carts import Cart
User = get_user_model()


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'eshop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = 'ecommerce'
        return context


class SignUpCreateView(generic.CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'custom-auth/form.html'
    success_message = "User Registration Success."
    title = "User Registration Form"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        with transaction.atomic():
            self.object.save()
            self.create_user_profile(user=self.object)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_default_redirect_url())

    def get_default_redirect_url(self, **kwargs):
        """Return the default redirect URL."""
        get_request = self.request.GET.copy()
        if get_request.get('next', None):
            self.next_page = get_request.get('next')
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
    
    def create_user_profile(self, *args, **kwargs):
        user_obj = kwargs['user']
        try:
            UserProfile.objects.create(user=user_obj, created_by=user_obj)
        except Exception as e:
            pass
    

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'custom-auth/form.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Login successfully'
    title = "User Login Form"
    next_page = None

    def get_default_redirect_url(self, **kwargs):
        """Return the default redirect URL."""
        get_request = self.request.GET.copy()
        if get_request.get('next', None):
            self.next_page = get_request.get('next')
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, self.success_message)
        log_obj = CustomLogEntry()
        log_obj.log_addition(self.request, form.get_user(), self.success_message)
        return HttpResponseRedirect(self.get_default_redirect_url())    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print("User is authenticated")
            return HttpResponseRedirect(self.success_url)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserLogoutView(View):
    next_page = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        current_cart = copy.deepcopy(cart.cart)
        current_coupon = copy.deepcopy(cart.coupon)
        auth_logout(request)
        cart.restore_after_logout(current_cart, current_coupon)
        return HttpResponseRedirect(self.next_page)


class UserPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy(settings.LOGIN_URL)
    template_name = 'custom-auth/form.html'
    title = 'Password change form'
    success_message = 'Password Change successfully'


""" custom error view start from here """

def custom_page_not_found(request, exception, template_name='custom-auth/error.html'):
    code = "404"
    title = "page not found"
    message = "The page you requested could not be found."
    context = {
        'error_code': code,
        'error_title': title,
        'error_message': message,
    }
    return render(request, template_name, context)

def custom_server_error(request, template_name='custom-auth/error.html'):
    code = "500"
    title = "Server Error"
    message = "An error occurred while processing your request."
    context = {
        'error_code': code,
        'error_title': title,
        'error_message': message,
    }
    return render(request, template_name, context)

def custom_permission_denied_view(request, template_name='custom-auth/error.html'):
    code = "403"
    title = "Forbidden! permission denied"
    message = "You don't have permission to access the requested resource."
    context = {
        'error_code': code,
        'error_title': title,
        'error_message': message,
    }
    return render(request, template_name, context)

def custom_bad_request_view(request, template_name='custom-auth/error.html'):
    code = "400"
    title = "bad request"
    message = "Your browser sent a request that this server could not understand."
    context = {
        'error_code': code,
        'error_title': title,
        'error_message': message,
    }
    return render(request, template_name, context)