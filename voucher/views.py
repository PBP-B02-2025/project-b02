from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Voucher
from .forms import VoucherForm
import json

@login_required(login_url='/login/')
def voucher_view(request):
    vouchers = Voucher.objects.all().order_by('-id')
    context = {
        'active_page': 'voucher',
        'vouchers': vouchers,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'voucher.html', context)

@login_required(login_url='/login/')
@require_POST
def create_voucher_ajax(request):
    # Only superuser can create voucher
    if not request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'message': 'Anda tidak memiliki izin untuk membuat voucher!'
        }, status=403)
    
    try:
        # Parse data dari AJAX request
        kode = request.POST.get('kode')
        deskripsi = request.POST.get('deskripsi')
        persentase_diskon = request.POST.get('persentase_diskon')
        is_active = request.POST.get('is_active') == 'true'
        
        # Validasi data
        if not kode or not persentase_diskon:
            return JsonResponse({
                'status': 'error',
                'message': 'Kode dan persentase diskon wajib diisi!'
            }, status=400)
        
        # Cek apakah kode sudah ada
        if Voucher.objects.filter(kode=kode).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Kode voucher sudah ada!'
            }, status=400)
        
        # Buat voucher baru
        voucher = Voucher.objects.create(
            kode=kode,
            deskripsi=deskripsi,
            persentase_diskon=persentase_diskon,
            is_active=is_active
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Voucher berhasil dibuat!',
            'voucher': {
                'id': voucher.id,
                'kode': voucher.kode,
                'deskripsi': voucher.deskripsi,
                'persentase_diskon': str(voucher.persentase_diskon),
                'is_active': voucher.is_active
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }, status=500)

@login_required(login_url='/login/')
@require_POST
def update_voucher_ajax(request, voucher_id):
    # Only superuser can update voucher
    if not request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'message': 'Anda tidak memiliki izin untuk mengubah voucher!'
        }, status=403)
    
    try:
        voucher = get_object_or_404(Voucher, id=voucher_id)
        
        kode = request.POST.get('kode')
        deskripsi = request.POST.get('deskripsi')
        persentase_diskon = request.POST.get('persentase_diskon')
        is_active = request.POST.get('is_active') == 'true'
        
        # Validasi data
        if not kode or not persentase_diskon:
            return JsonResponse({
                'status': 'error',
                'message': 'Kode dan persentase diskon wajib diisi!'
            }, status=400)
        
        # Cek apakah kode sudah ada (kecuali untuk voucher ini sendiri)
        if Voucher.objects.filter(kode=kode).exclude(id=voucher_id).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Kode voucher sudah ada!'
            }, status=400)
        
        # Update voucher
        voucher.kode = kode
        voucher.deskripsi = deskripsi
        voucher.persentase_diskon = persentase_diskon
        voucher.is_active = is_active
        voucher.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Voucher berhasil diupdate!',
            'voucher': {
                'id': voucher.id,
                'kode': voucher.kode,
                'deskripsi': voucher.deskripsi,
                'persentase_diskon': str(voucher.persentase_diskon),
                'is_active': voucher.is_active
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }, status=500)

@login_required(login_url='/login/')
@require_POST
def delete_voucher_ajax(request, voucher_id):
    # Only superuser can delete voucher
    if not request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'message': 'Anda tidak memiliki izin untuk menghapus voucher!'
        }, status=403)
    
    try:
        voucher = get_object_or_404(Voucher, id=voucher_id)
        voucher_kode = voucher.kode
        voucher.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Voucher {voucher_kode} berhasil dihapus!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }, status=500)

def get_vouchers_json(request):
    vouchers = Voucher.objects.all().order_by('-id')
    vouchers_list = []
    for voucher in vouchers:
        vouchers_list.append({
            'id': voucher.id,
            'kode': voucher.kode,
            'deskripsi': voucher.deskripsi,
            'persentase_diskon': str(voucher.persentase_diskon),
            'is_active': voucher.is_active
        })
    return JsonResponse({'vouchers': vouchers_list})
