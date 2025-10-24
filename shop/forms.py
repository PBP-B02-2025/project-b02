# Di file baru: shop/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Tentukan field apa saja yang ingin Anda tampilkan di form
        # 'user' akan kita isi otomatis dari view
        fields = [
            'name', 
            'price', 
            'size', 
            'brand', 
            'description', 
            'category', 
            'thumbnail',
        ]
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Tambahkan styling/class Bootstrap (jika Anda pakai) atau class Anda sendiri
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-ajax'