from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import DetailedPortfolioSerializer, DetailedOrderSerializer, \
    DetailedCompleteOrderSerializer, DetailedIncompleteOrderSerializer, \
    BasicOrderSerializer
from .models import Portfolio, Order, Company, CompleteOrder, IncompleteOrder


class UserPortfolioAPI(generics.ListAPIView):
    """
    List of User's Portafolio
    """
    serializer_class = DetailedPortfolioSerializer

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(client_dni=user.dni)


class UserOrdersAPI(generics.ListAPIView):
    """
    List of User's Orders
    """
    serializer_class = DetailedOrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(client_dni=user.dni)


class UserOrdersByCompanyAPI(generics.ListAPIView):
    """
    List of User's Orders filtered by Company
    """
    serializer_class = DetailedOrderSerializer

    def get_queryset(self):
        user = self.request.user
        company = get_object_or_404(Company, acronym=self.kwargs['company'])
        return Order.objects.filter(client_dni=user.dni, company_ruc=company)


class NewOrderAPI(generics.GenericAPIView):
    """
    Create New Order for current User
    """
    serializer_class = BasicOrderSerializer

    def post(self, request, *args, **kwargs):
        # Preprocess input
        data = request.data
        data["client_dni"] = self.request.user.dni
        # Validate and create order
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # Create associated incomplete order
        incomplete_order = IncompleteOrder.objects.create(order, IncompleteOrder.OrderStatus.PENDING)
        response = DetailedIncompleteOrderSerializer(incomplete_order)
        # Return incomplete order serialized data
        return Response(response.data)





