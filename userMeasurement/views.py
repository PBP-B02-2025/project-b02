from django.shortcuts import render, redirect, get_object_or_404
from userMeasurement.forms import UserMeasurementForm
from userMeasurement.models import userMeasurement
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from shop.models import Product
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def show_measurement(request):
    if not request.user.is_authenticated:
        return render(request, 'recommended_size_guest.html', {'active_page': 'shop-size'})
    
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()
    products = []

    if not data:
        return render(request, 'recommended_size.html', {'data': None, 'active_page': 'shop-size'})

    product_type = request.GET.get('type', 'clothes')

    if product_type == 'clothes' and data.clothes_size:
        products = Product.objects.filter(category='Shirt', size=data.clothes_size)
    elif product_type == 'helmet' and data.helmet_size:
        products = Product.objects.filter(category='Helmet', size=data.helmet_size)

    return render(request, 'recommended_size.html', {
        'data': data,
        'products': products,
        'selected_type': product_type,
        'active_page': 'shop-size'
    })

@login_required(login_url='/login')
def get_recommended_products_json(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()
    product_type = request.GET.get('type', 'clothes')

    if not data:
        return JsonResponse({'error': 'No measurement data found'}, status=400)

    if product_type == 'clothes' and data.clothes_size:
        products = Product.objects.filter(category__iexact='shirt', size=data.clothes_size)
    elif product_type == 'helmet' and data.helmet_size:
        products = Product.objects.filter(category__iexact='helmet', size=data.helmet_size)
    else:
        products = []

    product_list = [{
        'id': p.id,
        'name': p.name,
        'size': p.size,
        'price': p.price,
        'thumbnail': p.thumbnail,
        'category': p.category,
    } for p in products]

    return JsonResponse({'status': 'success', 'products': product_list})

@login_required(login_url='/login')
def update_measurement(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UserMeasurementForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.calculate_clothes_size()
            obj.calculate_helmet_size()
            obj.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # kirim data yang diperbarui supaya JS bisa update DOM
                return JsonResponse({
                    'status': 'success',
                    'message': 'Data ukuran berhasil diperbarui!',
                    'measurement': {
                        'height': obj.height,
                        'weight': obj.weight,
                        'waist': obj.waist,
                        'hip': obj.hip,
                        'chest': obj.chest,
                        'head_circumference': obj.head_circumference,
                        'clothes_size': obj.clothes_size,
                        'helmet_size': obj.helmet_size,
                    }
                })
            # Non-AJAX
            return redirect('userMeasurement:show_measurement')

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # kirim error form
                errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)

    else:
        # GET request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # kirim data awal untuk preload form
            return JsonResponse({
                'status': 'ok',
                'measurement': {
                    'height': data.height,
                    'weight': data.weight,
                    'waist': data.waist,
                    'hip': data.hip,
                    'chest': data.chest,
                    'head_circumference': data.head_circumference,
                    'clothes_size': data.clothes_size,
                    'helmet_size': data.helmet_size,
                }
            })
        else:
            form = UserMeasurementForm(instance=data)
            return render(request, 'form.html', {'form': form})


@login_required(login_url='/login')
def delete_measurement(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    data = userMeasurement.objects.filter(user=request.user).first()
    if not data:
        return JsonResponse({'status': 'error', 'message': 'Tidak ada data untuk dihapus'})

    data.delete()
    return JsonResponse({'status': 'success', 'message': 'Data ukuran berhasil dihapus'})



