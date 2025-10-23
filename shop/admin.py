from django.contrib import admin
from .models import Product # <-- Ganti ini dengan nama model Anda

# Baris ini yang akan membuat model Anda muncul di admin
admin.site.register(Product)

# Jika Anda punya model lain, daftarkan juga:
# from .models import Product, Category
#
# admin.site.register(Product)
# admin.site.register(Category)