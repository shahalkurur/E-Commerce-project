# Generated by Django 4.2.6 on 2024-01-23 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0021_alter_products_dis_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='old_price',
            field=models.FloatField(null=True),
        ),
    ]
