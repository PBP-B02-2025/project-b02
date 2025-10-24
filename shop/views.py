# Di file shop/views.py

from django.shortcuts import render, get_object_or_404, redirect # Tambahkan redirect
from django.contrib import messages # Tambahkan messages
from .models import Product, Transaction
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from voucher.models import Voucher
from decimal import Decimal

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
        'selected_category': selected_category,       
        'current_filter_params': current_filter_params,
        'active_page': 'shop-classic',  # <-- ini yang bikin parent SHOP aktif
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
        'any_vouchers_exist': Voucher.objects.filter(is_active=True).exists()
    }
    
    return render(request, 'shop/product_detail.html', context)

@login_required
def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Keamanan: Pastikan hanya pemilik produk yang bisa mengedit
    if product.user != request.user:
        messages.error(request, "Anda tidak diizinkan mengedit produk ini.")
        return redirect('shop:product-detail', product_id=product.id)

    if request.method == 'POST':
        # Isi form dengan data baru (request.POST) dan data lama (instance=product)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil diperbarui!")
            return redirect('shop:product-detail', product_id=product.id)
    else:
        # Tampilkan form yang sudah terisi data lama
        form = ProductForm(instance=product)
        
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'shop/edit_product.html', context)


@login_required
def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Keamanan: Pastikan hanya pemilik produk yang bisa menghapus
    if product.user != request.user:
        messages.error(request, "Anda tidak diizinkan menghapus produk ini.")
        return redirect('shop:product-detail', product_id=product.id)

    # Kita hanya proses jika method-nya POST
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Produk '{product_name}' telah berhasil dihapus.")
        return redirect('shop:shop-main') # Redirect ke halaman shop utama
    
    # Jika user akses via GET, redirect kembali ke halaman detail
    return redirect('shop:product-detail', product_id=product.id)

@login_required
def transaction_history_view(request):
    """
    Menampilkan riwayat transaksi milik user yang sedang login.
    """
    # 1. Ambil semua transaksi milik user, urutkan dari yang paling baru
    #    Kita pakai .select_related('product') agar lebih efisien
    #    (Model Transaction sudah di-order by '-purchase_timestamp' di Meta)
    user_transactions = Transaction.objects.filter(user=request.user).select_related('product')
    
    context = {
        'transactions': user_transactions,
        'active_page': 'shop-history', # Untuk menandai link nav
    }
    
    # 2. Render template baru yang akan kita buat
    return render(request, 'shop/riwayat_transaksi.html', context)

@login_required
def create_transaction_ajax_view(request):
    if not request.method == 'POST':
        return JsonResponse({'status': 'error', 'message': 'Metode request tidak valid'}, status=405)

    try:
        # 1. Ambil data dari request POST
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        voucher_code = request.POST.get('voucher_code', '').strip()
        
        if quantity < 1:
            return JsonResponse({'status': 'error', 'message': 'Kuantitas tidak valid.'}, status=400)

        # 2. Ambil objek
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        # 3. --- PROSES VOUCHER (BAGIAN YANG DIPERBARUI) ---
        voucher_obj = None
        discount_percentage = Decimal('0.0') 
        
        if voucher_code:
            try:
                # Langkah A: Cari voucher berdasarkan KODE saja
                voucher_obj = Voucher.objects.get(kode=voucher_code)
                
                # Langkah B: Periksa apakah voucher-nya aktif
                if not voucher_obj.is_active:
                    # Ini adalah pesan error baru yang spesifik
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Voucher yang Anda masukkan sudah tidak aktif.'
                    }, status=400)
                
                # Langkah C: Jika aktif, ambil diskonnya
                discount_percentage = voucher_obj.persentase_diskon
                
            except Voucher.DoesNotExist:
                # Jika kodenya tidak ditemukan sama sekali
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Kode Voucher tidak valid atau tidak ditemukan.'
                }, status=400)

        # 4. Kalkulasi Harga
        original_product_price = product.price # Ini adalah INT
        total_original_price = Decimal(original_product_price * quantity)
        discount_amount = (total_original_price * discount_percentage) / Decimal('100.0')
        final_price = total_original_price - discount_amount # Hasilnya adalah Decimal

        # 5. Buat Transaksi
        Transaction.objects.create(
            user=user,
            product=product,
            voucher=voucher_obj,
            used_voucher_code=voucher_obj.kode if voucher_obj else None,
            quantity=quantity,
            original_product_price=original_product_price,
            applied_discount_percentage=int(discount_percentage), 
            final_price=int(final_price) 
        )
        
        # 6. Kirim respon sukses
        return JsonResponse({
            'status': 'success', 
            'message': 'Transaksi berhasil dicatat! Anda akan diarahkan ke riwayat.'
        })

    except Exception as e:
        # Tangkap error jika ada
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)