from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from userMeasurement.models import userMeasurement
from shop.models import Product
from django.http import JsonResponse

class UserMeasurementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="12345")
        self.measurement = userMeasurement.objects.create(
            user=self.user,
            height=170,
            weight=65,
            waist=80,
            hip=90,
            chest=95,
            head_circumference=57,
            clothes_size="M",
            helmet_size="L",
        )
        self.product = Product.objects.create(
            name="Test Shirt",
            category="Shirt",
            size="M",
            price=100000,
            thumbnail="img.jpg",
        )

    def test_show_measurement_not_authenticated(self):
        response = self.client.get(reverse("userMeasurement:show_measurement"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recommended_size_guest.html")

    def test_show_measurement_authenticated_no_data(self):
        self.measurement.delete()
        self.client.login(username="tester", password="12345")
        response = self.client.get(reverse("userMeasurement:show_measurement"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recommended_size.html")

    def test_show_measurement_authenticated_with_data(self):
        self.client.login(username="tester", password="12345")
        response = self.client.get(reverse("userMeasurement:show_measurement"), {"type": "clothes"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recommended_size.html")
        self.assertIn("products", response.context)

    def test_get_recommended_products_json_no_data(self):
        self.client.login(username="tester", password="12345")
        self.measurement.delete()
        response = self.client.get(reverse("userMeasurement:get_recommended_products_json"))
        self.assertEqual(response.status_code, 400)

    def test_get_recommended_products_json_success(self):
        self.client.login(username="tester", password="12345")
        response = self.client.get(reverse("userMeasurement:get_recommended_products_json"), {"type": "clothes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_update_measurement_get_ajax(self):
        self.client.login(username="tester", password="12345")
        response = self.client.get(
            reverse("userMeasurement:update_measurement"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("measurement", response.json())

    def test_update_measurement_post_ajax(self):
        self.client.login(username="tester", password="12345")
        data = {
            "height": 175,
            "weight": 70,
            "waist": 82,
            "hip": 95,
            "chest": 100,
            "head_circumference": 58,
        }
        response = self.client.post(
            reverse("userMeasurement:update_measurement"),
            data,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_update_measurement_post_invalid(self):
        self.client.login(username="tester", password="12345")
        response = self.client.post(
            reverse("userMeasurement:update_measurement"),
            {},  # kosong supaya invalid
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

    def test_delete_measurement_invalid_method(self):
        self.client.login(username="tester", password="12345")
        response = self.client.get(reverse("userMeasurement:delete_measurement"))
        self.assertEqual(response.status_code, 405)

    def test_delete_measurement_success(self):
        self.client.login(username="tester", password="12345")
        response = self.client.post(reverse("userMeasurement:delete_measurement"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_delete_measurement_no_data(self):
        self.client.login(username="tester", password="12345")
        self.measurement.delete()
        response = self.client.post(reverse("userMeasurement:delete_measurement"))
        self.assertEqual(response.json()["status"], "error")
