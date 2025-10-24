import uuid
from django.db import models
from django.contrib.auth.models import User
from voucher.models import Voucher

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    CATEGORY_CHOICES = [
        ('Shirt', 'Shirt'),
        ('Shoes', 'Shoes'),
        ('Water Bottle', 'Water Bottle'),
        ('Helmet', 'Helmet'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=10)
    brand = models.CharField(max_length=255, null=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lainnya')
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def _str_(self):
        return self.name

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="sales")
    voucher = models.ForeignKey(
        Voucher, 
        on_delete=models.SET_NULL, 
        null=True,                 
        blank=True,                
        related_name="transactions"
    )
    used_voucher_code = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="Salinan kode voucher saat transaksi (untuk arsip)"
    )
    quantity = models.PositiveIntegerField(default=1)
    original_product_price = models.PositiveIntegerField(help_text="Harga produk saat dibeli")
    applied_discount_percentage = models.PositiveIntegerField(default=0, help_text="Diskon yang didapat saat itu")
    final_price = models.PositiveIntegerField(help_text="Harga final setelah diskon") 
    purchase_timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-purchase_timestamp'] 
    def __str__(self):
        return f"Transaksi {self.id} oleh {self.user.username}"