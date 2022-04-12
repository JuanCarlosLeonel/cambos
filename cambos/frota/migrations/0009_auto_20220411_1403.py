# Generated by Django 3.2.6 on 2022-04-11 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_setoresportal'),
        ('frota', '0008_abastecimento_responsavel'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compras_pedido_id', models.IntegerField(db_column='compras_pedido_id', null=True)),
                ('compras_produto_id', models.IntegerField(db_column='compras_produto_id', null=True)),
            ],
            options={
                'db_table': 'souzacambos"."compras_pedido_items',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='motorista',
            name='empilhadeirista',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='empilhadeira',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=80)),
                ('quantidade', models.IntegerField(blank=True, null=True)),
                ('data_inicial', models.DateField(blank=True, null=True)),
                ('data_final', models.DateField(blank=True, null=True)),
                ('hora_inicial', models.TimeField(blank=True, null=True)),
                ('hora_final', models.TimeField(blank=True, null=True)),
                ('tipo_servico', models.CharField(choices=[('Ordem Serviço', 'Ordem Serviço'), ('Manutençao', 'Manutenção')], max_length=20, null=True)),
                ('tipo_manutencao', models.CharField(choices=[('Preventiva', 'Preventiva'), ('Corretiva', 'Corretiva')], max_length=20, null=True)),
                ('empilhadeira', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='frota.veiculo')),
                ('motorista', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='frota.motorista')),
            ],
            options={
                'db_table': 'frota"."empilhadeira_servico',
            },
        ),
        migrations.CreateModel(
            name='Ordem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=80)),
                ('quantidade', models.IntegerField(blank=True, null=True)),
                ('situacao', models.CharField(choices=[('1', 'Aberto'), ('2', 'Em atendimento'), ('3', 'Finalizado')], max_length=1)),
                ('observacao', models.CharField(max_length=80, null=True)),
                ('created_at', models.DateTimeField()),
                ('servico', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='frota.servicos')),
                ('setor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.setoresportal')),
            ],
            options={
                'db_table': 'frota"."empilhadeira_ordem',
            },
        ),
        migrations.CreateModel(
            name='ManutencaoEmpilhadeira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('botijaoreposto', models.CharField(max_length=2)),
                ('botijaoutilizado', models.CharField(max_length=2)),
                ('responsavel', models.TextField(max_length=100)),
                ('empilhadeira', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frota.veiculo')),
            ],
            options={
                'db_table': 'frota"."empilhadeira_manutencao',
            },
        ),
    ]