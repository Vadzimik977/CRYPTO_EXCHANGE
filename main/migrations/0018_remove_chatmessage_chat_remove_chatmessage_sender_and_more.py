# Generated by Django 4.2.4 on 2023-08-31 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_chatmessage_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
