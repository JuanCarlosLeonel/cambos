# Generated by Django 3.0.7 on 2021-05-15 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210515_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='ativo',
            field=models.BooleanField(default=False),
        ),
    ]
