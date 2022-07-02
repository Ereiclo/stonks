# Generated by Django 4.0.4 on 2022-06-23 20:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_remove_completeorder_price_per_stock_order_avg_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='avg_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 23, 15, 40, 23, 471149)),
        ),
    ]