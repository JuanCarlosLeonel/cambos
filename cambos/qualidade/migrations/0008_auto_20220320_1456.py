# Generated by Django 3.2.6 on 2022-03-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualidade', '0007_qualidadebot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qualidadebot',
            name='pedido_parado',
        ),
        migrations.AddField(
            model_name='qualidadebot',
            name='pedido_parado',
            field=models.BooleanField(default=False),
        ),
    ]
