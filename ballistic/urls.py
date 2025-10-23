# Di dalam file ballistic/urls.py

from django.contrib import admin
# Tambahkan 'include' di sini
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/', include('review.urls')),
    path('', include('main.urls')),     # Ini untuk homepage Anda
    path('shop/', include('shop.urls')), # <-- TAMBAHKAN BARIS INI
    path('forum/', include('forum.urls')),
    path('voucher/', include('voucher.urls')),
]
