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
        # Crear usuario en BD
        # Usar endpoint de user sin estar loggeado
        # Assert respuesta de error
        # Usar endpoint de login
        # Usar Token de login para acceder a endpoint de user
        # Assert respuesta de exito
        pass

