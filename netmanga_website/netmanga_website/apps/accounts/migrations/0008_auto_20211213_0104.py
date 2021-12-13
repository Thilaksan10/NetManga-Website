# Generated by Django 3.1.13 on 2021-12-13 01:04

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20211207_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creator',
            name='earned_money',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
    ]