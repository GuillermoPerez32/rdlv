# Generated by Django 4.1.1 on 2023-08-02 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_order_pay_type_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
