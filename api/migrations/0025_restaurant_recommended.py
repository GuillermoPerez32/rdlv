# Generated by Django 4.1.1 on 2023-08-13 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_order_was_paid_by_distributor_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='recommended',
            field=models.BooleanField(default=False, verbose_name='recommended'),
        ),
    ]
