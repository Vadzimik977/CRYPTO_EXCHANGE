# Generated by Django 4.2.4 on 2023-08-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_order_id_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
