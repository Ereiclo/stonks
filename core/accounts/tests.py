from atexit import register
from hashlib import sha512
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from knox.models import AuthToken
import base64


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

        register_url = reverse('register')
        register_data = {
            'username': 'TestUser',
            'password': 'TestPassword',
            'email': 'test@test.com'
        }
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

        login_url = reverse('login')
        bad_login_data = {
            'username': 'TestUser',
            'password': 'BadPassword'
        }
        response = self.client.post(login_url, bad_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        good_login_data = {
            'username': 'TestUser',
            'password': 'TestPassword'
        }
        response = self.client.post(login_url, good_login_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint intentando logear con contraseña erronea
        # Assert respuesta de error
        # Usar endpoint de login con contraseña correcta
        # Assert respuesta de exito
        pass

    def test_logout_account(self):
        """
        Ensure we can logout of current session.
        """
        register_url = reverse('register')
        register_data = {
            'username': 'TestUser',
            'password': 'TestPassword',
            'email': 'test@test.com'
        }
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

        login_url = reverse('login')
        login_data = {
            'username': 'TestUser',
            'password': 'TestPassword'
        }
        response = self.client.post(login_url, login_data, format = 'json')
        response = JsonResponse(str(response))
        token = str(response.content[54:118])[2:-1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_token = AuthToken.objects.all()[1].token_key
        self.assertEqual(token[:8], db_token)

        logout_url = reverse('logout')
        AUTH_TOKEN = "Token " + db_token
        self.client.credentials(HTTP_AUTHORIZATION = AUTH_TOKEN)

        
        # Crear usuario en BD
        # Usar endpoint para logear usuario
        # Assert token generado en BD
        # Usar endpoint para logout usuario
        # Assert token invalido
        pass

    def test_logoutall_account(self):
        """
        Ensure we can create a new account object.
        """
        # Crear usuario en BD
        # Usar endpoint para logear usuario (token 1)
        # Usar endpoint para logear usuario (token 2)
        # Usar endpoint para logout usuario con token 1
        # Assert token 2 invalido
        pass

    def test_token_validation(self):
        """
        Ensure the created token can be used to access-session restricted resources.
        """
        user_url = reverse('user')

        response = self.client.get(user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        register_url = reverse('register')
        register_data = {
            'username': 'TestUser',
            'password': 'TestPassword',
            'email': 'test@test.com'
        }
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')
        
        login_url = reverse('login')
        login_data = {
            'username': 'TestUser',
            'password': 'TestPassword'
        }
        response = self.client.post(login_url, login_data, format = 'json')
        token = str(response.content[54:118])[2:-1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        AUTH_TOKEN = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION = AUTH_TOKEN)
        response = self.client.get(user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint de user sin estar loggeado
        # Assert respuesta de error
        # Usar endpoint de login
        # Usar Token de login para acceder a endpoint de user
        # Assert respuesta de exito
        pass

