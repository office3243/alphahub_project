# Generated by Django 2.2 on 2019-08-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190817_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='other_charges',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_charges',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PL', 'Order Placed'), ('RC', 'Received'), ('PK', 'Packing'), ('SH', 'Shipped'), ('CN', 'Cancelled')], default='PL', max_length=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]