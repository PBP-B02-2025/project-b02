# Di file shop/urls.py

from django.urls import path
from . import views

app_name = 'shop' 

urlpatterns = [
    path('', views.shop_main_view, name='shop-main'),
    path('add-product-ajax/', views.add_product_ajax_view, name='add-product-ajax'),
]