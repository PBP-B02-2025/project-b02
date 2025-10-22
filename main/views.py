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

def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def register_user(request):
    return render(request, 'register.html')

def login_user(request):
    return render(request, 'login.html')

def login_ajax(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': '/'
            })
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid username or password.'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def logout_user(request):
    logout(request)
    response = redirect('/') 
    response.delete_cookie('last_login')
    return response