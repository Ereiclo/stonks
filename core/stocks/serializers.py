from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import serializers
from .models import Company, Portfolio, Order, IncompleteOrder, CompleteOrder


class BasicCompanySerializer(serializers.ModelSerializer):
    """
    Basic serializer for Company
    """
    class Meta:
        model = Company
        fields = ('ruc', 'company_name', 'acronym', 'lastest_price', )


class DetailedPortfolioSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Portfolio
    """
    company_ruc = BasicCompanySerializer(many=False, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('company_ruc', 'quantity')


class BasicCompleteOrderSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Complete Order
    """
    class Meta:
        model = CompleteOrder
        fields = ('price_per_stock', 'order_id', )
        extra_kwargs = {'order_id': {'write_only': True}, }


class BasicIncompleteOrderSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Incomplete Order
    """
    class Meta:
        model = IncompleteOrder
        fields = ('status', 'order_id',)
        extra_kwargs = {'order_id': {'write_only': True}, }


class BasicOrderSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Complete Order
    """
    class Meta:
        model = Order
        fields = ('client_dni', 'company_ruc', 'quantity', 'price',
                  'transaction_type',)
        extra_kwargs = {'client_dni': {'write_only': True},
                        'company_ruc': {'write_only': True}, }


class DetailedOrderSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Order
    """
    company_ruc = BasicCompanySerializer(many=False, read_only=True)
    incompleteorder = BasicIncompleteOrderSerializer(many=False, read_only=True)
    completeorder = BasicCompleteOrderSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('client_dni', 'company_ruc', 'quantity', 'price',
                  'transaction_type', 'incompleteorder', 'completeorder')
        extra_kwargs = {'client_dni': {'write_only': True}, }

