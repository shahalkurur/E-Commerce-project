# Generated by Django 4.2.6 on 2024-01-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'pending'), ('Processing', 'processing'), ('Complete', 'complete'), ('Out for shipping', 'out for shipping'), ('Delivered', 'delivered'), ('Cancel', 'cancel')], default='pending', max_length=150),
        ),
    ]
