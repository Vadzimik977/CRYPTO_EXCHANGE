# Generated by Django 4.2.4 on 2023-08-30 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, '😢'), (2, '😞'), (3, '😐'), (4, '😊'), (5, '😄')], default=0),
        ),
    ]
