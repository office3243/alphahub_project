# Generated by Django 2.2 on 2019-08-29 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_order_id', models.CharField(max_length=32)),
                ('txnid', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('gateway', models.CharField(choices=[('PT', 'Paytm')], default='PT', max_length=2)),
                ('status', models.CharField(choices=[('SC', 'Success'), ('FL', 'Failed')], default='IN', max_length=2)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
