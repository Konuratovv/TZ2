from django.contrib import admin
from django.urls import path, include
from .views import ProductAPIView, ProductsFilterAPIView, CartAPIView, OrderAPIView, CartListAPIView, OrderListAPIView

urlpatterns = [
    path('products/', ProductAPIView.as_view()),
    path('products/<int:pk>', ProductAPIView.as_view()),
    path('filter-products/', ProductsFilterAPIView.as_view()),
    path('add_to_cart/', CartAPIView.as_view()),
    path('order-from-cart/', OrderAPIView.as_view()),
    path('cart/', CartListAPIView.as_view()),
    path('orders/', OrderListAPIView.as_view())
]
