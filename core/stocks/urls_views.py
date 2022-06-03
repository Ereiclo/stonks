from django.urls import path, include
from . import api
from . import views


urlpatterns = [
    path('portfolio/',views.PortfolioView.as_view(),name="portfolio")

]




