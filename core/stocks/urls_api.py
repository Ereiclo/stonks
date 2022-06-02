from django.urls import path, include
from . import api

urlpatterns = [
    path('api/auth/register', api.UserPortafolioAPI.as_view(), name="api-portafolio" ),
]
