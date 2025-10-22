# Di dalam main/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')