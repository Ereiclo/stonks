from django.urls import path
from . import views

# -------------------------------- TEMPORARY --------------------------------


urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('user/', views.AccountView.as_view(), name="user"),
    path('update/', views.UpdateView.as_view(), name="update"),
    path('portfolio/',views.PortfolioView.as_view(),name="portfolio"),
]
