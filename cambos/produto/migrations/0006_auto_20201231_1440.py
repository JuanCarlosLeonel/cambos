# Generated by Django 3.0.7 on 2020-12-31 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_material_inativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desempenho',
            name='total_tingido',
            field=models.FloatField(blank=True, verbose_name='Total Tingido'),
        ),
    ]
