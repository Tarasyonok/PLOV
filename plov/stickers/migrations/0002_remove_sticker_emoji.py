# Generated by Django 5.1.7 on 2025-04-07 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stickers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sticker',
            name='emoji',
        ),
    ]
