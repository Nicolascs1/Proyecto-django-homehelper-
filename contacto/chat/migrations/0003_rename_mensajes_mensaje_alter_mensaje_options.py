# Generated by Django 5.1.3 on 2024-12-06 23:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_mensajes_delete_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mensajes',
            new_name='Mensaje',
        ),
        migrations.AlterModelOptions(
            name='mensaje',
            options={},
        ),
    ]
