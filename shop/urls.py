# Di file shop/urls.py

from django.urls import path
from . import views

app_name = 'shop' 

urlpatterns = [
    path('', views.shop_main_view, name='shop-main'),
    path('add-product-ajax/', views.add_product_ajax_view, name='add-product-ajax'),
    
    # --- TAMBAHKAN URL BARU INI ---
    # Ini adalah URL untuk halaman detail produk, cth: /shop/product/abc-123-xyz/
    path('product/<uuid:product_id>/', views.product_detail_view, name='product-detail'),
    path('product/<uuid:product_id>/edit/', views.edit_product_view, name='edit-product'),
    path('product/<uuid:product_id>/delete/', views.delete_product_view, name='delete-product'),
]