# Generated by Django 4.1.1 on 2023-07-02 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_product_time_alter_restaurant_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='categories_product',
            field=models.ManyToManyField(to='api.category', verbose_name='Products Categories'),
        ),
    ]
