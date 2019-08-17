# Generated by Django 2.2 on 2019-08-17 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_specification'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificationName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('unit', models.CharField(max_length=32)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
        migrations.AddField(
            model_name='specification',
            name='specification_name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='products.SpecificationName'),
            preserve_default=False,
        ),
    ]