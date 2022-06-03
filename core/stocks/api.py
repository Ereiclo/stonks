from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import PortafolioSerializer, OrderSerializer
from .models import Portfolio, Order, Company


class UserPortafolioAPI(generics.ListAPIView):
    serializer_class = PortafolioSerializer

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(client_dni=user.dni)


class UserOrderByCompanyAPI(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company, acronym=self.kwargs['company'])
        return Order.objects.filter(client_dni=user.dni, company_ruc=company)

