# Generated by Django 4.1.1 on 2023-07-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_restaurant_categories_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='um',
            field=models.CharField(default='', max_length=10, verbose_name='unit of measurement'),
            preserve_default=False,
        ),
    ]