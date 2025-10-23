# Di file shop/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product 
from django.core.paginator import Paginator
from django.http import JsonResponse                 # <-- 1. Import JsonResponse
from django.contrib.auth.decorators import login_required # <-- 2. Import login_required
from .forms import ProductForm                       # <-- 3. Import ProductForm baru kita

def shop_main_view(request):
    
    # --- 1. Ambil Kategori dari URL ---
    selected_category = request.GET.get('category')
    current_filter_params = "" # Ini untuk pagination
    
    # --- 2. Filter Queryset ---
    if selected_category:
        # Jika ada parameter 'category', filter produknya
        all_products_list = Product.objects.filter(category=selected_category).order_by('name')
        # Siapkan string untuk pagination
        current_filter_params = f"&category={selected_category}"
    else:
        # Jika tidak ada, tampilkan semua produk
        all_products_list = Product.objects.all().order_by('name')

    # --- 3. Pagination (setelah di-filter) ---
    paginator = Paginator(all_products_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    all_categories = Product.CATEGORY_CHOICES
    add_product_form = ProductForm()
    
    context = {
        'products': page_obj,
        'all_categories': all_categories,
        'add_product_form': add_product_form,
        'selected_category': selected_category,       # <-- Kirim kategori yg aktif
        'current_filter_params': current_filter_params, # <-- Kirim string filter
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

def product_detail_view(request, product_id):
    """
    View untuk menampilkan halaman detail dari satu produk.
    """
    # Ambil 1 produk berdasarkan ID, atau tampilkan halaman 404 jika tidak ada
    product = get_object_or_404(Product, id=product_id)
    
    # Import Review model and get reviews for this product
    from review.models import Review
    from review.forms import ReviewForm
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-id')
    form = ReviewForm()
    
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    
    return render(request, 'shop/product_detail.html', context)