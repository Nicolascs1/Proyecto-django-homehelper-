# Generated by Django 5.1.3 on 2024-12-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_quotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
