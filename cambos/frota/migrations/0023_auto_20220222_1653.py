# Generated by Django 3.2.6 on 2022-02-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0022_auto_20220217_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='abastecimento',
            name='interno',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='manutencao',
            name='km',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
