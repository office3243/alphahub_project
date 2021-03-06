# Generated by Django 2.2 on 2019-08-30 22:31

from django.db import migrations, models
import payments.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20190830_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_order_id',
            field=models.CharField(default=payments.models.payment_order_id_generator, max_length=64),
        ),
        migrations.AlterField(
            model_name='payment',
            name='txnid',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
