# Generated by Django 2.2 on 2019-08-21 01:09

from django.db import migrations, models
import products.validators


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20190819_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, validators=[products.validators.validate_nonzero]),
        ),
    ]