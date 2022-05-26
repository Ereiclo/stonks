from django.urls import path, include
from .api import RegisterAPI, LoginAPI, MainUser
from knox import views as knox_views

urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view(), name="register" ),
    path('api/auth/login', LoginAPI.as_view(), name="login"),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="logout"),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    #DEMO
    path('api/auth/user', MainUser.as_view(), name="user"),
]