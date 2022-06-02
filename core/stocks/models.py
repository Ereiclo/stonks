from django.db import models
from accounts.models import Client


class Company(models.Model):
    ruc = models.CharField(max_length=11, primary_key=True)
    acronym = models.CharField(max_length=12, unique=True)
    lastest_price = models.DecimalField(max_digits=7,decimal_places=2)
    stocks_for_client = models.ManyToManyField(Client, through="Portfolio")


class Portfolio(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = ('client_dni','company_ruc')


class Order(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    transaction_type = models.BooleanField()


class IncompleteOrder(models.Model):
    order_id = models.ForeignKey(Order,on_delete = models.CASCADE)
    status = models.CharField(max_length=1)


class CompleteOrder(models.Model):
    order_id = models.ForeignKey(Order,on_delete = models.CASCADE)
    price_per_stock = models.DecimalField(max_digits=7,decimal_places=2)
