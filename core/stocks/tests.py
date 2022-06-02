from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken as KnoxAuthToken
from accounts.models import Client
from .models import Portfolio, Company, Order


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

    orders1_data = [
        {
            'client_dni': user1_data['dni'],
            'company_ruc': companies_data[0]['ruc'],
            'quantity': 15,
            'price': 25.62,
            'transaction_type': Order.TransactionType.BUY_LIMIT,
        },
        {
            'client_dni': user1_data['dni'],
            'company_ruc': companies_data[1]['ruc'],
            'quantity': 20,
            'price': 23.41,
            'transaction_type': Order.TransactionType.SELL_STOP,
        },
    ]

    orders2_data = [
        {
            'client_dni': user2_data['dni'],
            'company_ruc': companies_data[0]['ruc'],
            'quantity': 11,
            'price': 78.94,
            'transaction_type': Order.TransactionType.BUY_MARKET,
        },
        {
            'client_dni': user2_data['dni'],
            'company_ruc': companies_data[1]['ruc'],
            'quantity': 19,
            'price': 65.21,
            'transaction_type': Order.TransactionType.SELL_LIMIT,
        },
    ]

    test_company = companies_data[0]['acronym']
    orders_by_company_url = reverse('api-order-by-company', args=[test_company, ])

    expected_orders1 = [orders1_data[0], ]
    expected_orders1[0]['transaction_type'] = str(expected_orders1[0]['transaction_type'])

    expected_orders2 = [orders2_data[0], ]
    expected_orders2[0]['transaction_type'] = str(expected_orders2[0]['transaction_type'])

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
            tmp = p.copy()
            tmp['client_dni'] = Client.objects.get(dni=p['client_dni'])
            tmp['company_ruc'] = Company.objects.get(ruc=p['company_ruc'])
            Portfolio.objects.create(**tmp)

    def utility_generate_orders(self, orders_list):
        """
        Create portafolio data.
        """
        for o in orders_list:
            tmp = o.copy()
            tmp['client_dni'] = Client.objects.get(dni=o['client_dni'])
            tmp['company_ruc'] = Company.objects.get(ruc=o['company_ruc'])
            Order.objects.create(**tmp)

    def utility_set_credentials(self, token):
        """
        Set credentials for authorization
        """
        auth_token = "Token " + token
        self.client.credentials(HTTP_AUTHORIZATION=auth_token)

    def utility_assert_equal_dict_response(self, dict_expected, response_data):
        self.assertEqual(len(response_data), len(dict_expected))
        dict_data_compare = [
            {str(key): str(value) for key, value in d.items()}
            for d in dict_expected
        ]
        response_data_compare = [
            {str(key): str(value) for key, value in d.items()}
            for d in response_data
        ]
        self.assertEqual(response_data_compare, dict_data_compare)

    def utility_assert_equal_portafolio(self, token, portafolio_data):
        self.utility_set_credentials(token=token)
        response = self.client.get(self.portafolio_url)
        self.utility_assert_equal_dict_response(portafolio_data, response.data)

    def utility_assert_equal_orders(self, token, orders_data):
        self.utility_set_credentials(token=token)
        response = self.client.get(self.orders_by_company_url)
        self.utility_assert_equal_dict_response(orders_data, response.data)

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

    def test_order(self):
        """
        Test Order
        """
        token_user1 = self.utility_generate_user_data_and_token(self.user1_data)
        token_user2 = self.utility_generate_user_data_and_token(self.user2_data)
        self.utility_generate_companies(self.companies_data)
        self.utility_generate_orders(self.orders1_data)
        self.utility_generate_orders(self.orders2_data)
        self.utility_assert_equal_orders(token_user1, self.expected_orders1)
        self.utility_assert_equal_orders(token_user2, self.expected_orders2)





