from atexit import register
from hashlib import sha512
from telnetlib import LOGOUT
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Client
from knox.models import AuthToken as KnoxAuthToken
import base64


class AccountTests(APITestCase):

    def setUp(self):
        super().__init__()
        self.register_url = reverse('api-register')
        self.login_url = reverse('api-login')
        self.user_url = reverse('api-user')
        self.logout_url = reverse('api-logout')
        self.logoutall_url = reverse('api-logoutall')

        self.register_data = {
            'dni': '12345678',
            'names': 'TestName',
            'lastname': 'TestLastName',
            'password': 'TestPassword',
            'email': 'test@test.com'
        }
        self.bad_login_data = {
            'username': '12345678',
            'password': 'BadPassword'
        }
        self.good_login_data = {
            'username': '12345678',
            'password': 'TestPassword'
        }

    def utility_create_user(self):
        """
        Create default user
        """
        return Client.objects.create_user(**self.register_data)

    def utility_create_token(self, client):
        """
        Create token for a user
        """
        token = KnoxAuthToken.objects.create(client)
        return token[1]

    def utility_set_credentials(self, token):
        """
        Set credentials for authorization
        """
        auth_token = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

    def test_register_account(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().dni, '12345678')
        self.assertEqual(Client.objects.get().email, 'test@test.com')

    def test_login_account(self):
        """
        Ensure we can login to existing account.
        """
        self.utility_create_user()
        response = self.client.post(self.login_url, self.bad_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.login_url, self.good_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_account(self):
        """
        Ensure we can logout of current session.
        """
        token = self.utility_create_token(self.utility_create_user())
        self.utility_set_credentials(token=token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logoutall_account(self):
        """
        Ensure we can create a new account object.
        """
        client = self.utility_create_user()
        token1 = self.utility_create_token(client)
        token2 = self.utility_create_token(client)

        self.utility_set_credentials(token = token1)
        response = self.client.post(self.logoutall_url)
        self.assertEqual(KnoxAuthToken.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.utility_set_credentials(token = token2)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Crear usuario en BD
        # Usar endpoint para logear usuario (token 1)
        # Usar endpoint para logear usuario (token 2)
        # Usar endpoint para logout usuario con token 1
        # Assert token 2 invalido

    def test_token_validation(self):
        """
        Ensure the created token can be used to access-session restricted resources.
        """
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        token = self.utility_create_token(self.utility_create_user())
        self.utility_set_credentials(token=token)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint de user sin estar loggeado
        # Assert respuesta de error
        # Usar endpoint de login
        # Usar Token de login para acceder a endpoint de user
        # Assert respuesta de exito
