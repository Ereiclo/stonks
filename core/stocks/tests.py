from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken as KnoxAuthToken
from accounts.models import Client
from .models import Portfolio, Company


class StocksTests(APITestCase):
    portafolio_url = reverse('api-portafolio')

    user1_data = {
        'dni': '12345678',
        'names': 'TestName',
        'lastname': 'TestLastName',
        'password': 'TestPassword',
        'email': 'test@test.com'
    }

    user2_data = {
        'dni': '87654321',
        'names': 'ExtraName',
        'lastname': 'ExtraLastName',
        'password': 'ExtraPassword',
        'email': 'extra@test.com'
    }

    companies_data = [
        {
            'ruc': '12345678901',
            'acronym': 'TST',
            'lastest_price': 52.50,
        },
        {
            'ruc': '12345678902',
            'acronym': 'MOV',
            'lastest_price': 28.30,
        },
    ]

    portafolio1_data = [
        {
            'client_dni': user1_data['dni'],
            'company_ruc': companies_data[0]['ruc'],
            'quantity': 5,
        },
        {
            'client_dni': user1_data['dni'],
            'company_ruc': companies_data[1]['ruc'],
            'quantity': 10,
        },
    ]

    portafolio2_data = [
        {
            'client_dni': user2_data['dni'],
            'company_ruc': companies_data[0]['ruc'],
            'quantity': 10,
        },
        {
            'client_dni': user2_data['dni'],
            'company_ruc': companies_data[1]['ruc'],
            'quantity': 20,
        },
    ]


    def utility_generate_user_data_and_token(self, user_data):
        """
        Create user and get auth token.
        """
        client = Client.objects.create_user(**user_data)
        token = KnoxAuthToken.objects.create(client)
        return token[1]

    def utility_generate_companies(self, companies_list):
        """
        Create companies.
        """
        for c in companies_list:
            Company.objects.create(**c)

    def utility_generate_portafolio(self, portafolio_list):
        """
        Create portafolio data.
        """
        for p in portafolio_list:
            client = Client.objects.get(dni=p['client_dni'])
            company = Company.objects.get(ruc=p['company_ruc'])
            quantity = p["quantity"]
            Portfolio.objects.create(client_dni=client, company_ruc=company, quantity=quantity)

    def utility_set_credentials(self, token):
        """
        Set credentials for authorization
        """
        auth_token = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

    def utility_assert_equal_portafolio(self, token, portafolio_data):
        self.utility_set_credentials(token=token)
        response = self.client.get(self.portafolio_url)
        self.assertEqual(len(response.data), len(portafolio_data))
        self.assertEqual(response.data, portafolio_data)

    def test_portafolio(self):
        """
        Test portafolio
        """
        token_user1 = self.utility_generate_user_data_and_token(self.user1_data)
        token_user2 = self.utility_generate_user_data_and_token(self.user2_data)
        self.utility_generate_companies(self.companies_data)
        self.utility_generate_portafolio(self.portafolio1_data)
        self.utility_generate_portafolio(self.portafolio2_data)
        self.utility_assert_equal_portafolio(token_user1, self.portafolio1_data)
        self.utility_assert_equal_portafolio(token_user2, self.portafolio2_data)






