from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CompletedOrderSerializer, DetailedPortfolioSerializer, DetailedOrderSerializer, \
    BasicOrderSerializer, BasicCompanySerializer 
from .models import CompleteOrder, Portfolio, Order, Company, IncompleteOrder
from .exception import UserNotEnoughMoney, UserNotEnoughStocks, UnexpectedOrderError
from .matching_service import matching_service
import decimal


class UserPortfolioAPI(generics.ListAPIView):
    """
    List of User's Portfolio
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




class UserCompletedOrders(generics.ListAPIView):
    """
    List of User's Completed Orders
    """
    serializer_class = CompletedOrderSerializer
    def get_queryset(self):
        user = self.request.user

        # print(CompleteOrder.objects.filter(order_id__client_dni = user.dni))
        return CompleteOrder.objects.filter(order_id__client_dni = user.dni)






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

        # Buy & Sell Validation Logic
        order_type = Order.TransactionType(serializer.validated_data["transaction_type"])
        user_money = decimal.Decimal(self.request.user.money)

        # Buy order
        if order_type.is_buy():
            # Check if user has enough money
            total_price = decimal.Decimal(serializer.validated_data["price"]) \
                          * decimal.Decimal(serializer.validated_data["quantity"])
            if user_money < total_price:
                raise UserNotEnoughMoney()

        # Sell order
        elif order_type.is_sell():
            # Check if user has enough stocks
            total_stocks = decimal.Decimal(
                get_object_or_404(Portfolio,
                                  client_dni=self.request.user.dni,
                                  company_ruc=serializer.validated_data["company_ruc"]).quantity
            )
            if total_stocks < serializer.validated_data["quantity"]:
                raise UserNotEnoughStocks()

        # Error
        else:
            raise UnexpectedOrderError()

        # Update DataBase
        # Create order & associated incomplete order
        order = serializer.save()
        order.quantity_left = order.quantity
        order = serializer.save()
        IncompleteOrder.objects.create(order_id=order, status=IncompleteOrder.OrderStatus.PENDING)
        # Return detailed order serialized data
        matching_service(order)
        response = DetailedOrderSerializer(order)
        return Response(response.data)


class CompaniesAPI(generics.ListAPIView):
    """
    List of Companies
    """
    permission_classes = (permissions.AllowAny,)

    serializer_class = BasicCompanySerializer
    queryset = Company.objects.all()
