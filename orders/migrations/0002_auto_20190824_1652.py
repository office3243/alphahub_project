# Generated by Django 2.2 on 2019-08-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, to='carts_app.CartItem'),
        ),
    ]