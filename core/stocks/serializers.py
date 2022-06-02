from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Company, Portfolio, Order


class PortafolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('client_dni', 'company_ruc', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client_dni', 'company_ruc', 'quantity', 'price', 'transaction_type')



