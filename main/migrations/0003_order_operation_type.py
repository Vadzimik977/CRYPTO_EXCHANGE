# Generated by Django 4.2.4 on 2023-08-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='operation_type',
            field=models.CharField(default='None', max_length=10),
        ),
    ]
