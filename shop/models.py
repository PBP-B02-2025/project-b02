import uuid
from django.db import models
from django.contrib.auth.models import User

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
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lainnya')
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def _str_(self):
        return self.name