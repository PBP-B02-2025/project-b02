# Di dalam file ballistic/urls.py

from django.contrib import admin
# Tambahkan 'include' di sini
from django.urls import path, include 

urlpatterns = [
    path('', include('main.urls')), # <-- TAMBAHKAN BARIS INI
    path('admin/', admin.site.urls),
    path('measurement/', include('userMeasurement.urls')),
    path('forum/', include('forum.urls')),
    path('shop/', include('shop.urls')), # <-- TAMBAHKAN BARIS INI
    path('voucher/', include('voucher.urls')),
]
