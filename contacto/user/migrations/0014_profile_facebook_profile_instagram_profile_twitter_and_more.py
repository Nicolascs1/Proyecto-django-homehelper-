# Generated by Django 5.1.3 on 2024-12-10 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Twitter'),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Página Web'),
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título de la Credencial')),
                ('file', models.FileField(upload_to='credentials/', verbose_name='Archivo de Credencial (PDF o Imagen)')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', to='user.profile')),
            ],
        ),
    ]
