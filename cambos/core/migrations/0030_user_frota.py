# Generated by Django 3.2.6 on 2021-12-21 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='frota',
            field=models.BooleanField(default=False),
        ),
    ]
