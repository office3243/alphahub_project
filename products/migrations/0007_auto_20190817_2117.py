# Generated by Django 2.2 on 2019-08-17 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20190817_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='name',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='preference',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='unit_name',
        ),
        migrations.AddField(
            model_name='product',
            name='extra_info',
            field=models.TextField(blank=True),
        ),
    ]
