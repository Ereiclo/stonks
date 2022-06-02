from django.urls import path, include
from . import api
from knox import views as knox_views

urlpatterns = [
    path('api/auth/register', api.RegisterAPI.as_view(), name="api-register" ),
    path('api/auth/login', api.LoginAPI.as_view(), name="api-login"),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="api-logout"),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view(), name='api-logoutall'),
    #DEMO
    path('api/auth/user', api.MainUser.as_view(), name="api-user"),
]
