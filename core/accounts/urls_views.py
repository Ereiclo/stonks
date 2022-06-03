from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="user-index"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('user/', views.AccountView.as_view(), name="user"),
    path('update/', views.UpdateView.as_view(), name="update")
]
