# Generated by Django 2.2 on 2019-08-30 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190830_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_expected',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NP', 'Payment Pending'), ('PL', 'Order Placed'), ('PK', 'Packing'), ('SH', 'Shipped'), ('CN', 'Cancelled')], default='NP', max_length=2),
        ),
    ]
