# Generated by Django 2.2 on 2019-08-24 16:52

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190824_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=orders.models.order_id_generator, max_length=32),
        ),
    ]