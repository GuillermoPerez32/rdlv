# Generated by Django 4.1.1 on 2023-07-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_product_um'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is active'),
        ),
    ]
