# Generated by Django 4.1.1 on 2023-07-24 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_order_user_alter_orderdetail_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]