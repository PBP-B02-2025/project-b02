from django import forms
from .models import Voucher

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['kode', 'deskripsi', 'persentase_diskon', 'is_active']
        widgets = {
            'kode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: PROMOHEMAT20',
                'required': True
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi voucher...',
                'rows': 3
            }),
            'persentase_diskon': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'max': '100.00',
                'required': True
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'kode': 'Kode Voucher',
            'deskripsi': 'Deskripsi',
            'persentase_diskon': 'Persentase Diskon (%)',
            'is_active': 'Voucher Aktif'
        }
