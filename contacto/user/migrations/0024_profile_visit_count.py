# Generated by Django 5.1.3 on 2024-12-19 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_user_comuna_user_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='visit_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
