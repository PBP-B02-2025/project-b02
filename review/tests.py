from django.test import TestCase, Client
from .models import Review
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
from shop.models import Product
import uuid
import review.urls
from django.urls import reverse
# Create your tests here.
from django.contrib.auth import get_user_model
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



from django.test import TestCase, Client
from .models import Review
# Create your tests here.

class FunctionalTest(LiveServerTestCase):

    User = get_user_model()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service(ChromeDriverManager().install())
        cls.browser = webdriver.Chrome(service=service)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Close browser after all tests complete
        cls.browser.quit()

    def tearDown(self):
        # Clean up browser state between tests
        self.browser.delete_all_cookies()
        self.browser.execute_script("window.localStorage.clear();")
        self.browser.execute_script("window.sessionStorage.clear();")
        # Navigate to blank page to reset state
        self.browser.get("about:blank")

    def setUp(self):
        # Create user for testing
        self.test_user = User.objects.create_user(
            username='testadmin',
            password='testpassword'
        )

        self.create_product()

        

    def create_product(self):

        self.test_product = Product.objects.create(
            id=uuid.uuid4(),         
            user=self.test_user,
            name="Sepatu Olahraga",
            price=350000,
            size="42",
            description="Sepatu nyaman untuk olahraga",
            category="Shoes",
            thumbnail="https://example.com/shoes.jpg",
            is_featured=True
        )

        

    def login_user(self):
        """Helper method to login user"""
        self.browser.get(f"{self.live_server_url}/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testadmin")
        password_input.send_keys("testpassword")
        password_input.submit()
        
    def test_add_review(self):
        self.login_user()

        post_data = {
            'comment': 'Test comment',
            'star': 4,
        }

        

        url = reverse('review:add_review', args=[self.test_product.id])


        response = self.client.post(url, data=post_data)
        # response = self.client.post(url, data=review)

        self.assertEqual(response.status_code, 201)

    # def test_news_detail(self):
    #     # Test news detail page

    #     # Login first because of @login_required decorator
    #     self.login_user()

    #     # Create news for testing
    #     review = Review.objects.create(
    #         title="Detail Test News",
    #         content="Content for detail testing",
    #         user=self.test_user
    #     )

    #     # Open news detail page
    #     self.browser.get(f"{self.live_server_url}/news/{news.id}/")

    #     # Check if detail page opens correctly
    #     self.assertIn("Detail Test News", self.browser.page_source)
    #     self.assertIn("Content for detail testing", self.browser.page_source)
