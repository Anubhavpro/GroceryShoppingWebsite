# Generated by Django 3.2.9 on 2022-11-17 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehome', '0011_auto_20221117_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(null=True),
        ),
    ]
