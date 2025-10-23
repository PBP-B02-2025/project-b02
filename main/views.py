# Di dalam main/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime

# Nama fungsi ini harus sama dengan yang di main/urls.py
def main_view(request):
    # Render file 'main.html' yang ada di 'main/templates/'
    # Django akan otomatis mencari di 'main/templates/main.html'
    return render(request, 'main.html')