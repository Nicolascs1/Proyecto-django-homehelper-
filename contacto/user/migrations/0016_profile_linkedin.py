# Generated by Django 5.1.3 on 2024-12-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_credential_description_alter_credential_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='LinkedIn'),
        ),
    ]
