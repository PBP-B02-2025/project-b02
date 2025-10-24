from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Voucher(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    kode = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Kode unik voucher, misal: PROMOHEMAT20"
    )
    
    deskripsi = models.TextField(
        blank=True, 
        help_text="Deskripsi singkat tentang voucher ini."
    )
    
    persentase_diskon = models.DecimalField(
        max_digits=5,         # misal: 100.00 (total 5 angka)
        decimal_places=2,     # 2 angka di belakang koma
        help_text="Persentase diskon, misal: 15.50 untuk 15.5%",
        validators=[
            MinValueValidator(0.01),   # Diskon minimal
            MaxValueValidator(100.00)  # Diskon maksimal 100%
        ]
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Tandai jika voucher ini aktif dan bisa digunakan"
    )

    def __str__(self): 
        status = "Aktif" if self.is_active else "Nonaktif"
        return f"{self.kode} ({self.persentase_diskon}% - {status})"

    class Meta:
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"