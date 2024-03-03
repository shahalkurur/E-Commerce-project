# Generated by Django 4.2.6 on 2024-01-16 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0012_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('discount', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
                ('mini_amount', models.IntegerField()),
            ],
        ),
    ]
