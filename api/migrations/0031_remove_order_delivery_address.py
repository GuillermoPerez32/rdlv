# Generated by Django 4.1.1 on 2023-08-22 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_remove_restaurant_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_address',
        ),
    ]
