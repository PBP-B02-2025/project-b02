from django.urls import path
from . import views

app_name = 'main'  # <-- TAMBAHKAN BARIS INI. INI ADALAH KUNCINYA.
from main.views import *
# Beri nama 'main' agar bisa dipanggil pakai {% url 'main:nama_url' %}
app_name = 'main' 

urlpatterns = [
    # Ini adalah view untuk homepage Anda
    path('', views.main_view, name='main-view'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('logout/', logout_user, name='logout')
]