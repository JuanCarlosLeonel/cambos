# Generated by Django 3.0.7 on 2021-08-18 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0012_custo_patrimonio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custo',
            name='patrimonio',
            field=models.FloatField(blank=True, default=0),
        ),
    ]