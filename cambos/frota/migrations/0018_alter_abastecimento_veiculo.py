# Generated by Django 3.2 on 2022-01-26 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0017_auto_20220126_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abastecimento',
            name='veiculo',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='frota.veiculo'),
        ),
    ]