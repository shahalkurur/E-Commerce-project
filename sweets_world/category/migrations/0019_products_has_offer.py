# Generated by Django 4.2.6 on 2024-01-23 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0018_products_dis_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='has_offer',
            field=models.BooleanField(default=False),
        ),
    ]
