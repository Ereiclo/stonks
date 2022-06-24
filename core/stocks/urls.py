from django.urls import path, include
from . import api

urlpatterns = [
    path('portfolio/', api.UserPortfolioAPI.as_view(), name="api-portafolio"),
    path('orders/', api.UserOrdersAPI.as_view(), name="api-orders"),
    path('orders/<str:company>/', api.UserOrdersByCompanyAPI.as_view(), name="api-orders-by-company"),
    path('new-order/', api.NewOrderAPI.as_view(), name="api-new-order"),
    path('companies/', api.CompaniesAPI.as_view(), name="api-companies"),
    path('user-completed-orders/', api.UserCompletedOrders.as_view(), name="api-user-completed-orders"),
]
