from django.db import models
from accounts.models import Client


class Company(models.Model):
    ruc = models.CharField(max_length=11, primary_key=True)
    acronym = models.CharField(max_length=12)
    lastest_price = models.FloatField()
    stocks_for_client = models.ManytoManyField(Client, through="Portfolio")


class Portfolio(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.Cascade)
    company_ruc = models.ForeignKey(Company, on_delete=models.Cascade)
    quantity = models.IntegerField()


class Order(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.Cascade)
    company_ruc = models.ForeignKey(Company, on_delete=models.Cascade)


quantity = models.IntegerField()
price = models.FloatField()
transaction_type = models.BooleanField()


class IncompleteOrder(models.Model):
    order_id = models.ForeignKey(Order)
    status = models.CharField(max_length=1)


class CompleteOrder(models.Model):
    order_id = models.ForeignKey(Order)
    price_per_stock = models.FloatField()
