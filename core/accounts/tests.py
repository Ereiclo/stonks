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

    register_url = reverse('register')
    login_url = reverse('login')
    user_url = reverse('user')

    register_data = {
        'username': 'TestUser',
        'password': 'TestPassword',
        'email': 'test@test.com'
    }
    bad_login_data = {
        'username': 'TestUser',
        'password': 'BadPassword'
    }
    good_login_data = {
        'username': 'TestUser',
        'password': 'TestPassword'
    }

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

    def test_login_account(self):
        """
        Ensure we can create a new account object.
        """
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

        login_url = reverse('login')

        response = self.client.post(login_url, self.bad_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(login_url, self.good_login_data, format='json')
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
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')


        response = self.client.post(self.login_url, self.good_login_data, format='json')
        response = JsonResponse(response.data)
        token = str(response.content[54:118])[2:-1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        db_token = AuthToken.objects.all()[1].token_key
        self.assertEqual(token[:8], db_token)

        logout_url = reverse('logout')
        auth_token = "Token " + db_token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

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

        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

        response = self.client.post(self.login_url, self.good_login_data, format='json')
        token = str(response.content[54:118])[2:-1]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        auth_token = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)
        response = self.client.get(self.user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint de user sin estar loggeado
        # Assert respuesta de error
        # Usar endpoint de login
        # Usar Token de login para acceder a endpoint de user
        # Assert respuesta de exito
        pass
