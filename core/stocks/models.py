from django.db import models
from accounts.models import Client
from django.utils.translation import gettext_lazy as _
from datetime import datetime,date
from django.core.validators import RegexValidator

acronym_validator = RegexValidator(r'[A-Z]{1,12}', 'Acrónimo inválido')


class Company(models.Model):
    ruc = models.CharField(max_length=11, primary_key=True)
    acronym = models.CharField(max_length=12, unique=True, validators=[acronym_validator])
    company_name = models.CharField(max_length=64)
    lastest_price = models.DecimalField(max_digits=7, decimal_places=2)
    stocks_for_client = models.ManyToManyField(Client, through="Portfolio")


class Portfolio(models.Model):
    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    avg_price = models.DecimalField(max_digits=7, decimal_places=2,default=0)

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

        def is_buy(self):
            return str(self)[0] == 'B'

        def is_sell(self):
            return str(self)[0] == 'S'

        def is_market_order(self):
            return str(self)[1] == 'M'

        def is_limit_order(self):
            return str(self)[1] == 'L'

        def is_stop_order(self):
            return str(self)[1] == 'S'

    client_dni = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_ruc = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices)
    avg_price = models.DecimalField(max_digits=7, decimal_places=2,default=0)
    quantity_left = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now())



class IncompleteOrder(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        CANCELLED = 'C', _('Cancelled')

    order_id = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=1, choices=OrderStatus.choices)


class CompleteOrder(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
