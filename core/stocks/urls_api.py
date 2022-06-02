from django.urls import path, include
from . import api

urlpatterns = [
    path('portafolio/', api.UserPortafolioAPI.as_view(), name="api-portafolio" ),
    path('orders/<str:company>/', api.UserOrderByCompanyAPI.as_view(), name="api-order-by-company")
]
