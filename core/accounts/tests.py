from atexit import register
from hashlib import sha512
from telnetlib import LOGOUT
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from knox.models import AuthToken
import base64


class AccountTests(APITestCase):

    register_url = reverse('api-register')
    login_url = reverse('api-login')
    user_url = reverse('api-user')
    logout_url = reverse('api-logout')
    logoutall_url = reverse('api-logoutall')

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

    def utility_test_register(self):
        """
        Test registration of new account.
        """
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'TestUser')
        self.assertEqual(User.objects.get().email, 'test@test.com')

    def utility_test_login(self):
        """
        Login and create token for a user
        """
        response = self.client.post(self.login_url, self.good_login_data, format='json')
        token = response.data["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return token

    def utility_set_credentials(self, token):
        """
        Set credentials for authorization
        """
        auth_token = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

    def utility_test_logout(self, token):
        """
        Logout user
        """
        self.utility_set_credentials(token=token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        self.utility_test_register()

    def test_login_account(self):
        """
        Ensure we can create a new account object.
        """
        self.utility_test_register()



        response = self.client.post(self.login_url, self.bad_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.login_url, self.good_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint intentando logear con contraseña erronea
        # Assert respuesta de error
        # Usar endpoint de login con contraseña correcta
        # Assert respuesta de exito

    def test_logout_account(self):
        """
        Ensure we can logout of current session.
        """
        self.utility_test_register()


        token = self.utility_test_login()

        self.utility_test_logout(token = token)
        # Crear usuario en BD
        # Usar endpoint para logear usuario
        # Assert token generado en BD
        # Usar endpoint para logout usuario
        # Assert token invalido

    def test_logoutall_account(self):
        """
        Ensure we can create a new account object.
        """
        self.utility_test_register()

        token1 = self.utility_test_login()
        token2 = self.utility_test_login()

        self.utility_set_credentials(token = token1)
        response = self.client.post(self.logoutall_url)
        self.assertEqual(AuthToken.objects.count(), 0)
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

        self.utility_test_register()

        token = self.utility_test_login()

        self.utility_set_credentials(token=token)
        
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Crear usuario en BD
        # Usar endpoint de user sin estar loggeado
        # Assert respuesta de error
        # Usar endpoint de login
        # Usar Token de login para acceder a endpoint de user
        # Assert respuesta de exito
