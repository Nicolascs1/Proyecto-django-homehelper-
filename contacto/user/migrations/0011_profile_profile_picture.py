# Generated by Django 5.1.3 on 2024-12-09 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_profile_specialties_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='media/profile_default.png', upload_to='media/'),
        ),
    ]
