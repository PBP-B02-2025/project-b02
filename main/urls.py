from django.urls import path
from main.views import *

app_name = 'main'  # <-- TAMBAHKAN BARIS INI. INI ADALAH KUNCINYA.

urlpatterns = [
    # Ini adalah view untuk homepage Anda
    path('', main_view, name='main-view'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('logout/', logout_user, name='logout')
]