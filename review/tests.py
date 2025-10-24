from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.http import JsonResponse
from .models import Review
from .forms import ReviewForm
from shop.models import Product
import json


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.product = Product.objects.create(
            user=self.user, 
            name="Test Product", 
            price=100, 
            size=8, 
            brand="Test Brand", 
            category="Shirt", 
            description="A product for testing", 
            thumbnail="http://example.com/image.jpg"
        )

    def test_str_representation(self):
        review = Review.objects.create(
            comment="Great product!", 
            user=self.user, 
            product=self.product, 
            star=4
        )
        expected_str = f"Review by {self.user.username} for {self.product.name}"
        self.assertEqual(str(review), expected_str)
    
    def test_review_creation(self):
        """Test creating a review with valid data"""
        review = Review.objects.create(
            comment="Excellent quality!",
            user=self.user,
            product=self.product,
            star=5
        )
        self.assertEqual(review.comment, "Excellent quality!")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.star, 5)
        self.assertTrue(review.id)  # Check UUID is generated
    
    def test_star_validation(self):
        """Test star rating validation (should be between 0-5)"""
        # Valid star ratings
        for star in [0, 1, 2, 3, 4, 5]:
            review = Review(
                comment=f"Test comment for {star} stars",
                user=self.user,
                product=self.product,
                star=star
            )
            review.full_clean()  # Should not raise ValidationError
    
    def test_review_relationship(self):
        """Test foreign key relationships"""
        review = Review.objects.create(
            comment="Test relationship",
            user=self.user,
            product=self.product,
            star=3
        )
        # Test user relationship
        self.assertEqual(review.user.username, "tester")
        # Test product relationship
        self.assertEqual(review.product.name, "Test Product")
        # Test reverse relationship
        self.assertIn(review, self.product.review_set.all())


class ReviewFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="12345")
        self.product = Product.objects.create(
            user=self.user,
            name="Test Product",
            price=100,
            size=8,
            brand="Test Brand",
            category="Shirt",
            description="A product for testing",
            thumbnail="http://example.com/image.jpg"
        )
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'comment': 'This is a great product!',
            'star': 5
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_comment(self):
        """Test form with empty comment"""
        form_data = {
            'comment': '',
            'star': 4
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)
    
    def test_invalid_star_rating(self):
        """Test form with invalid star rating"""
        form_data = {
            'comment': 'Test comment',
            'star': 6  # Invalid - should be 0-5
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('star', form.errors)
    
    def test_long_comment(self):
        """Test form with comment exceeding max length"""
        long_comment = 'x' * 251  # Exceeds 250 char limit
        form_data = {
            'comment': long_comment,
            'star': 3
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)


class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="12345")
        self.other_user = User.objects.create_user(username="other", password="12345")
        self.product = Product.objects.create(
            user=self.user,
            name="Test Product",
            price=100,
            size=8,
            brand="Test Brand",
            category="Shirt",
            description="A product for testing",
            thumbnail="http://example.com/image.jpg"
        )
    
    def test_add_review_requires_login(self):
        """Test that adding review requires authentication"""
        url = reverse('review:add_review', kwargs={'product_id': self.product.id})
        response = self.client.post(url, {
            'comment': 'Test comment',
            'star': 5
        })
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_add_review_authenticated_user(self):
        """Test adding review with authenticated user"""
        self.client.login(username="tester", password="12345")
        url = reverse('review:add_review', kwargs={'product_id': self.product.id})
        
        response = self.client.post(url, {
            'comment': 'Great product!',
            'star': 5
        })
        
        # Check if review was created
        self.assertTrue(Review.objects.filter(
            user=self.user,
            product=self.product,
            comment='Great product!'
        ).exists())
    
    def test_add_review_ajax_success(self):
        """Test AJAX review submission success"""
        self.client.login(username="tester", password="12345")
        url = reverse('review:add_review', kwargs={'product_id': self.product.id})
        
        response = self.client.post(url, {
            'comment': 'AJAX test review',
            'star': 4
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('Review added successfully', data['message'])
    
    def test_add_review_ajax_invalid_data(self):
        """Test AJAX review submission with invalid data"""
        self.client.login(username="tester", password="12345")
        url = reverse('review:add_review', kwargs={'product_id': self.product.id})
        
        response = self.client.post(url, {
            'comment': '',  # Empty comment - invalid
            'star': 4
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
    
    def test_delete_review_own_review(self):
        """Test deleting own review"""
        # Create a review
        review = Review.objects.create(
            comment="Test review",
            user=self.user,
            product=self.product,
            star=3
        )
        
        self.client.login(username="tester", password="12345")
        url = reverse('review:delete_review', kwargs={'id': review.id})
        
        response = self.client.delete(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Check review was deleted
        self.assertFalse(Review.objects.filter(id=review.id).exists())
    
    def test_delete_review_other_user_review(self):
        """Test attempting to delete another user's review"""
        # Create a review by other user
        review = Review.objects.create(
            comment="Other user's review",
            user=self.other_user,
            product=self.product,
            star=4
        )
        
        self.client.login(username="tester", password="12345")
        url = reverse('review:delete_review', kwargs={'id': review.id})
        
        response = self.client.delete(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('Permission denied', data['message'])
        
        # Check review still exists
        self.assertTrue(Review.objects.filter(id=review.id).exists())
    
    def test_edit_review_get(self):
        """Test GET request to edit review page"""
        review = Review.objects.create(
            comment="Original comment",
            user=self.user,
            product=self.product,
            star=3
        )
        
        self.client.login(username="tester", password="12345")
        url = reverse('review:edit_review', kwargs={'id': review.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original comment")

    def test_edit_review_non_user(self):
        """Test that a user cannot edit another user's review"""
        review = Review.objects.create(
            comment="Other user's comment",
            user=self.other_user,
            product=self.product,
            star=4
        )
        
        self.client.login(username="tester", password="12345")
        url = reverse('review:edit_review', kwargs={'id': review.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Should return 404 Not Found
    
    def test_show_all_reviews_of_product(self):
        """Test displaying all reviews for a product"""
        Review.objects.create(
            comment="First review",
            user=self.user,
            product=self.product,
            star=5
        )
        Review.objects.create(
            comment="Second review",
            user=self.other_user,
            product=self.product,
            star=4
        )
        
        url = reverse('review:show_product_reviews', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First review")
        self.assertContains(response, "Second review")

    def test_read_review_json(self):
        """Test reading review data as JSON"""
        review = Review.objects.create(
            comment="JSON test review",
            user=self.user,
            product=self.product,
            star=5
        )
        
        url = reverse('review:read_review_by_json', kwargs={'id': review.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['comment'], "JSON test review")
        self.assertEqual(data['star'], 5)
        self.assertEqual(data['user'], str(self.user))
        self.assertEqual(data['product'], str(self.product))


class ReviewIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="12345")
        self.product = Product.objects.create(
            user=self.user,
            name="Integration Test Product",
            price=150,
            size=10,
            brand="Test Brand",
            category="Shirt",
            description="Product for integration testing",
            thumbnail="http://example.com/image.jpg"
        )
    
    def test_complete_review_workflow(self):
        """Test complete workflow: create, read, edit, delete review"""
        self.client.login(username="tester", password="12345")
        
        # 1. Create review
        add_url = reverse('review:add_review', kwargs={'product_id': self.product.id})
        response = self.client.post(add_url, {
            'comment': 'Initial review comment',
            'star': 4
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 201)
        review = Review.objects.get(user=self.user, product=self.product)
        
        # 2. Read review
        read_url = reverse('review:read_review_by_json', kwargs={'id': review.id})
        response = self.client.get(read_url)
        self.assertEqual(response.status_code, 200)
        
        # 3. Edit review
        edit_url = reverse('review:edit_review', kwargs={'id': review.id})
        response = self.client.post(edit_url, {
            'comment': 'Updated review comment',
            'star': 5
        })
        
        review.refresh_from_db()
        self.assertEqual(review.comment, 'Updated review comment')
        self.assertEqual(review.star, 5)
        
        # 4. Delete review
        delete_url = reverse('review:delete_review', kwargs={'id': review.id})
        response = self.client.delete(delete_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

