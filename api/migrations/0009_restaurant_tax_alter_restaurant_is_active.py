# Generated by Django 4.1.1 on 2023-07-07 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_restaurant_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='tax',
            field=models.FloatField(default=10, verbose_name='tax'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
