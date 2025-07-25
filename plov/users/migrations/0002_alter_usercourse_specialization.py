# Generated by Django 5.2 on 2025-04-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='specialization',
            field=models.CharField(
                choices=[
                    ('D', 'Веб-разработка на Django'),
                    ('M', 'Машинное обучение'),
                    ('B', 'Большие данные'),
                    ('G', 'Веб-разработка на Go'),
                    ('A', 'Анализ данных'),
                ],
                default='D',
            ),
        ),
    ]
