# Generated by Django 4.2.4 on 2023-08-28 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_order_processed_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='processed',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=20),
        ),
    ]
