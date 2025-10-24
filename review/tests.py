from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Review
from shop.models import Product


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.product = Product.objects.create(user = self.user, name="Test Product", price=100, size=8, brand="Test Brand", category="Shirt", description="A product for testing", thumbnail="http://example.com/image.jpg")


    def test_str_representation(self):
        review = Review.objects.create(comment="Great product!", user=self.user, product=self.product, star=4)
        self.assertEqual(str(review.comment), "Great product!")
