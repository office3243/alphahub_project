# Generated by Django 2.2 on 2019-08-24 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190824_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='uuid',
        ),
    ]
