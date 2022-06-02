from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Company, Portfolio


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('acronym', 'lastest_price')


class PortafolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('client_dni', 'company_ruc', 'quantity')

