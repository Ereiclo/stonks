from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import serializers
from .models import Company, Portfolio, Order


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('company_name', 'lastest_price')


class PortafolioSerializer(serializers.ModelSerializer):
    company_ruc = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('company_ruc', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('client_dni', 'company_ruc', 'quantity', 'price', 'transaction_type')



