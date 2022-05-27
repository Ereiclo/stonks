from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        register_url = reverse('register')
        data = {
            'username': 'DemoUser',
            'password': 'S3cUR3P422W0rD',
            'email': 'demo@gmail.com',
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'DemoUser')
        self.assertEqual(User.objects.get().email, 'demo@gmail.com')

    def test_login_account(self):
        """
        Ensure we can create a new account object.
        """
        pass

    def test_token_validation(self):
        """
        Ensure the created token can be used to access-session restricted resources.
        """
        pass
