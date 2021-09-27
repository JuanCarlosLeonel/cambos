# Generated by Django 3.2.6 on 2021-09-27 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roupa', '0015_useretapa'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapa',
            name='padrao',
            field=models.BooleanField(default=False, verbose_name='Padrão'),
        ),
        migrations.AlterField(
            model_name='processo',
            name='status_spi',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
