# Generated by Django 3.2.6 on 2022-03-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualidade', '0009_qualidadetrack'),
    ]

    operations = [
        migrations.AddField(
            model_name='qualidadebot',
            name='ver_acoes',
            field=models.BooleanField(default=False),
        ),
    ]
