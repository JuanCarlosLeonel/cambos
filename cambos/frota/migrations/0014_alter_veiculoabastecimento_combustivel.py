# Generated by Django 3.2 on 2022-01-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0013_auto_20220114_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veiculoabastecimento',
            name='combustivel',
            field=models.CharField(choices=[('Diesel', 'Diesel'), ('Gasolina', 'Gasolina'), ('Álcool', 'Álcool')], max_length=40),
        ),
    ]