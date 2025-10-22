import uuid
from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('promo', 'Promo'),
        ('product_update', 'Product Update'),
        ('event', 'Event'),
        ('training_tips', 'Training Tips'),
        ('sports_news', 'Sports News'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)  # 🆕 nama penulis
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sports_news')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def short_content(self):
        """Menampilkan hanya sebagian dari konten untuk preview"""
        return self.content[:100] + "..." if len(self.content) > 100 else self.content

    def increment_views(self):
        self.news_views += 1
        self.save()
