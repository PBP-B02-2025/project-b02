from django.shortcuts import render, redirect, get_object_or_404
from userMeasurement.forms import UserMeasurementForm
from userMeasurement.models import userMeasurement
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from shop.models import Product
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='/login')
def show_measurement(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()
    products = []

    if not data:
        return render(request, 'recommended_size.html', {'data': None})

    # Ambil tipe produk dari query param
    product_type = request.GET.get('type', 'clothes')  # default: clothes

    if product_type == 'clothes' and data.clothes_size:
        products = Product.objects.filter(category='Shirt', size=data.clothes_size)
    elif product_type == 'helmet' and data.helmet_size:
        products = Product.objects.filter(category='Helmet', size=data.helmet_size)

    return render(request, 'recommended_size.html', {
        'data': data,
        'products': products,
        'selected_type': product_type
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
            return redirect('userMeasurement:show_measurement')
    else:
        form = UserMeasurementForm(instance=data)

    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def delete_measurement(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()

    if data:
        data.delete()
        messages.success(request, "Data ukuran berhasil dihapus.")
    else:
        messages.warning(request, "Tidak ada data untuk dihapus.")

    return redirect('userMeasurement:show_measurement')




