# Di dalam main/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime

# Nama fungsi ini harus sama dengan yang di main/urls.py
def main_view(request):
    # Render file 'main.html' yang ada di 'main/templates/'
    # Django akan otomatis mencari di 'main/templates/main.html'
    context = {
        'active_page': 'home'
    }
    return render(request, 'main.html', context)

def register_user(request):
    form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    
    context = {'form': form}
    return render(request, 'register.html', context)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validasi
        if not username or not password1 or not password2:
            return JsonResponse({
                'success': False,
                'error': 'All fields are required.'
            }, status=400)
        
        if password1 != password2:
            return JsonResponse({
                'success': False,
                'error': 'Passwords do not match.',
                'errors': {'password2': ['Passwords do not match.']}
            }, status=400)
        
        if len(password1) < 8:
            return JsonResponse({
                'success': False,
                'error': 'Password must be at least 8 characters long.',
                'errors': {'password1': ['Password must be at least 8 characters long.']}
            }, status=400)
        
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Username already exists.',
                'errors': {'username': ['Username already exists.']}
            }, status=400)
        
        try:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Account created successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error creating account: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            response = redirect('main:main-view')
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    
    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Username and password are required.'
            }, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': '/'  # Redirect ke halaman home
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid username or password.',
                'errors': {
                    'username': ['Invalid credentials'],
                    'password': ['Invalid credentials']
                }
            }, status=401)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=400)

def logout_user(request):
    logout(request)
    response = redirect('main:login')
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login/')
def profil_view(request):
    # Import userMeasurement model
    from userMeasurement.models import userMeasurement
    
    # Coba ambil data measurement user
    try:
        measurement = userMeasurement.objects.get(user=request.user)
    except userMeasurement.DoesNotExist:
        measurement = None
    
    context = {
        'active_page': 'profil',
        'measurement': measurement
    }
    return render(request, 'profil.html', context)
