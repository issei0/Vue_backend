# Generated by Django 4.0.2 on 2022-02-20 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
    ]
