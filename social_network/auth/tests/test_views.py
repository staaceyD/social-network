from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ActivityViewTests(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=user)

    def test_get_user_activity(self):
        url = reverse("activity")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("last_request_at", response.json())
        self.assertIn("last_login_at", response.json())
