# Buat file baru di main/urls.py

from django.urls import path
from . import views

# Beri nama 'main' agar bisa dipanggil pakai {% url 'main:nama_url' %}
app_name = 'main' 

urlpatterns = [
    # Path '' (kosong) berarti ini adalah homepage untuk aplikasi 'main'
    path('', views.main_view, name='main-view'),
]