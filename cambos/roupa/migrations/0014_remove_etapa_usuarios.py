# Generated by Django 3.1.13 on 2021-09-25 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roupa', '0013_etapa_usuarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etapa',
            name='usuarios',
        ),
    ]