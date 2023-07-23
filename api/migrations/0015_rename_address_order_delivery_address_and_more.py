# Generated by Django 4.1.1 on 2023-07-22 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_configuration_distributor_is_online_product_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='delivery_address',
        ),
        migrations.AlterField(
            model_name='configuration',
            name='exchange_rate',
            field=models.FloatField(default=0, verbose_name='exchange rate'),
        ),
    ]
