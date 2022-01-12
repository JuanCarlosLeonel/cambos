# Generated by Django 3.2.6 on 2021-12-21 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0002_veiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('origem', models.CharField(max_length=40)),
                ('destino', models.CharField(max_length=40)),
                ('carga', models.CharField(max_length=40)),
                ('peso', models.FloatField()),
                ('km_inicial', models.IntegerField()),
                ('km_final', models.IntegerField()),
                ('motorista', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='frota.motorista')),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='frota.veiculo')),
            ],
            options={
                'db_table': 'frota"."viagem',
            },
        ),
    ]
