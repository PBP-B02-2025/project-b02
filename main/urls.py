from django.urls import path
from . import views

app_name = 'main'  # <-- TAMBAHKAN BARIS INI. INI ADALAH KUNCINYA.

urlpatterns = [
    # Ini adalah view untuk homepage Anda
    path('', views.main_view, name='main-view'),
]