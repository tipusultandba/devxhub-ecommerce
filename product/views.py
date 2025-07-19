from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value, Count
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
import datetime
from .models import Product
# from cart.carts import Cart

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .serializer import ProductSerializer


def format_search_string(fields, keyword):
    Qr = None
    for field in fields:        
        q = Q(**{"%s__icontains" % field: keyword })
        if Qr:
            Qr = Qr | q
        else:
            Qr = q    
    return Qr


class ProductListView(generic.ListView):
    permission_required = 'product.view_product'
    model = Product
    context_object_name = 'items'
    paginate_by = 9
    template_name = 'eshop/shop.html'
    queryset = Product.objects.all()
    search_fields = ['title',]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # product search start from here.
        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['all_product_count'] = self.queryset.count()
        return context
    


class ProductDetailView(generic.DetailView):
    permission_required = 'eshop.view_product'
    model = Product
    context_object_name = 'item'
    template_name = 'eshop/detail.html'
    # queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.get_queryset().count()
        context['basic_template'] = ""
        return context


class ProductListApiView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductSerializer
    queryset= Product.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset