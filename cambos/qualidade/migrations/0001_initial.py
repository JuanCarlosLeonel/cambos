# Generated by Django 3.2.6 on 2022-03-15 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roupa', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaCorte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lacre', models.IntegerField()),
                ('ficha_corte', models.CharField(blank=True, max_length=7, null=True)),
                ('dados', models.JSONField()),
            ],
            options={
                'db_table': 'qualidade"."FichaCorte',
            },
        ),
        migrations.CreateModel(
            name='TabelaAmostragem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'qualidade"."tabelaamostragem',
            },
        ),
        migrations.CreateModel(
            name='ItemTabelaAmostragem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_minima', models.IntegerField()),
                ('quantidade_maxima', models.IntegerField()),
                ('amostragem', models.IntegerField()),
                ('tabela_amostragem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qualidade.tabelaamostragem')),
            ],
            options={
                'db_table': 'qualidade"."itemtabelaamostragem',
            },
        ),
        migrations.CreateModel(
            name='Inspecao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20)),
                ('volume', models.CharField(choices=[('Total', 'Total'), ('Percentual', 'Percentual'), ('Tabela', 'Tabela')], default='Percentual', max_length=10)),
                ('percentual_amostragem', models.IntegerField()),
                ('criterio_aprovacao', models.IntegerField()),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roupa.processo')),
                ('tabela', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qualidade.tabelaamostragem')),
            ],
            options={
                'db_table': 'qualidade"."inspecao',
            },
        ),
        migrations.CreateModel(
            name='Auditor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auditor_externo', models.CharField(blank=True, max_length=20, null=True)),
                ('auditor_interno', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.pessoa')),
                ('oficina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='roupa.etapa')),
            ],
            options={
                'db_table': 'qualidade"."auditor',
            },
        ),
    ]
