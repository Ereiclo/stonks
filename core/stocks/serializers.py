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
        fields = ('company_name', 'acronym', 'lastest_price', )


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
        fields = ('price_per_stock', )


class BasicIncompleteOrderSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Incomplete Order
    """
    class Meta:
        model = IncompleteOrder
        fields = ('status', 'order',)


class BasicOrderSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Incomplete Order
    """
    company_ruc = BasicCompanySerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('client_dni', 'company_ruc', 'quantity', 'price',
                  'transaction_type',)
        extra_kwargs = {'client_dni': {'write_only': True}, }


class DetailedCompleteOrderSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Complete Order
    """
    order = BasicOrderSerializer(many=False, read_only=True)

    class Meta:
        model = CompleteOrder
        fields = ('price_per_stock', 'order', )


class DetailedIncompleteOrderSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Incomplete Order
    """
    order = BasicOrderSerializer(many=False, read_only=True)

    class Meta:
        model = IncompleteOrder
        fields = ('status', 'order', )


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



