# Generated by Django 3.0.7 on 2021-05-02 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comercial', '0002_auto_20210307_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cotacao',
            options={'verbose_name_plural': 'Cotações'},
        ),
        migrations.AlterModelOptions(
            name='customanipulacao',
            options={'verbose_name_plural': 'Custo Manipulações'},
        ),
        migrations.AlterModelOptions(
            name='itemcotacao',
            options={'verbose_name_plural': 'Itens Cotações'},
        ),
        migrations.AlterModelOptions(
            name='pontuacaoproducao',
            options={'verbose_name_plural': 'Pontuação Produção'},
        ),
        migrations.AlterModelOptions(
            name='precotecido',
            options={'verbose_name_plural': 'Preço Tecidos'},
        ),
    ]
