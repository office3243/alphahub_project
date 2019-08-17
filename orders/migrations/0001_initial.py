# Generated by Django 2.2 on 2019-08-14 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=264)),
                ('line_2', models.CharField(max_length=264)),
                ('locality', models.CharField(max_length=64)),
                ('city', models.CharField(default='Pune', max_length=64)),
                ('state', models.CharField(default='Maharashtra', max_length=64)),
                ('zip_code', models.CharField(max_length=6)),
                ('phone', models.CharField(max_length=13)),
                ('address_type', models.CharField(choices=[('SH', 'Shop or Office'), ('HM', 'Home')], max_length=2)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_charges', models.DecimalField(decimal_places=2, max_digits=7)),
                ('other_charges', models.DecimalField(decimal_places=2, max_digits=7)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PL', 'Placed'), ('PR', 'Process'), ('SH', 'Shipped'), ('CN', 'Cancelled')], max_length=2)),
                ('is_payed', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.Address')),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.OrderProduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]