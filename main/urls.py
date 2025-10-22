# Buat file baru di main/urls.py

from django.urls import path
from . import views
from main.views import register_ajax, register, login
# Beri nama 'main' agar bisa dipanggil pakai {% url 'main:nama_url' %}
app_name = 'main' 

urlpatterns = [
    # Path '' (kosong) berarti ini adalah homepage untuk aplikasi 'main'
    path('', views.main_view, name='main-view'),
    path('register_ajax/', register_ajax, name='register_ajax'),
    path('register/', register, name='register'),
    path('login/', login, name='login')
]