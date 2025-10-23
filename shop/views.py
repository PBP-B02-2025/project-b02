# Di file shop/views.py

from django.shortcuts import render
from .models import Product 
from django.core.paginator import Paginator
from django.http import JsonResponse                 # <-- 1. Import JsonResponse
from django.contrib.auth.decorators import login_required # <-- 2. Import login_required
from .forms import ProductForm                       # <-- 3. Import ProductForm baru kita

def shop_main_view(request):
    all_products_list = Product.objects.all().order_by('name')
    
    paginator = Paginator(all_products_list, 9) # <-- (Anda ganti jadi 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    all_categories = Product.CATEGORY_CHOICES
    
    # --- 4. TAMBAHKAN INI ---
    # Buat instance form kosong untuk modal
    add_product_form = ProductForm()
    # -----------------------
    
    context = {
        'products': page_obj,
        'all_categories': all_categories,
        'add_product_form': add_product_form, # <-- 5. Kirim form ke template
    }
    
    return render(request, 'shop/shop.html', context)


# --- 6. BUAT VIEW BARU DI BAWAHNYA ---

@login_required # Pastikan hanya user yang login bisa tambah produk
def add_product_ajax_view(request):
    # Hanya izinkan request POST
    if request.method == 'POST':
        # 'request.POST' berisi data dari form
        form = ProductForm(request.POST) 
        
        if form.is_valid():
            # Simpan form tapi jangan commit dulu
            product = form.save(commit=False)
            # Set 'user' nya secara manual
            product.user = request.user 
            product.save()
            
            # Kirim respon sukses
            return JsonResponse({'status': 'success', 'message': 'Produk berhasil ditambahkan!'})
        else:
            # Jika form tidak valid, kirim errornya
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    # Jika bukan POST, kirim error
    return JsonResponse({'status': 'error', 'message': 'Metode request tidak valid'}, status=405)