# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-17 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.CharField(max_length=255),
        ),
    ]
