from django.db import models
from accounts.models import Client
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    ruc = models.CharField(max_length=11, primary_key=True)
    acronym = models.CharField(max_length=12, unique=True)
    lastest_price = models.DecimalField(max_digits=7, decimal_places=2)
    stocks_for_client = models.ManyToManyField(Client, through="Portfolio")


class Portfolio(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('client_dni', 'company_ruc')


class Order(models.Model):
    class TransactionType(models.TextChoices):
        BUY_MARKET = 'BM', _('Buy Market')
        BUY_LIMIT = 'BL', _('Buy Limit')
        BUY_STOP = 'BS', _('Buy Stop')
        SELL_MARKET = 'SM', _('Sell Market')
        SELL_LIMIT = 'SL', _('Sell Limit')
        SELL_STOP = 'SS', _('Sell Stop')

    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices)


class IncompleteOrder(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=1)


class CompleteOrder(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_per_stock = models.DecimalField(max_digits=7, decimal_places=2)
