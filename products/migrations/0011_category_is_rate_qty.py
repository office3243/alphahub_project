# Generated by Django 2.2 on 2019-08-21 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20190821_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_rate_qty',
            field=models.BooleanField(default=False, verbose_name='Allow only rate quantities'),
        ),
    ]