from django.test import TestCase, Client
from .models import Review
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
# import product di sini nanti

# Create your tests here.

from django.test import TestCase, Client
from .models import Review
# Create your tests here.

class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        # Create user for testing
        self.test_user = User.objects.create_user(
            username='testadmin',
            password='testpassword'
        )

    def create_product():

        self.test_product = Prod

        

    def login_user(self):
        """Helper method to login user"""
        self.browser.get(f"{self.live_server_url}/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testadmin")
        password_input.send_keys("testpassword")
        password_input.submit()

    def test_news_detail(self):
        # Test news detail page

        # Login first because of @login_required decorator
        self.login_user()

        # Create news for testing
        review = Review.objects.create(
            title="Detail Test News",
            content="Content for detail testing",
            user=self.test_user
        )

        # Open news detail page
        self.browser.get(f"{self.live_server_url}/news/{news.id}/")

        # Check if detail page opens correctly
        self.assertIn("Detail Test News", self.browser.page_source)
        self.assertIn("Content for detail testing", self.browser.page_source)
