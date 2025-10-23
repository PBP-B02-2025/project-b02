from django.contrib import admin
from .models import Voucher

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('kode', 'persentase_diskon', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('kode', 'deskripsi')
