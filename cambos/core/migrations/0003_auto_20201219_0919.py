# Generated by Django 3.0.7 on 2020-12-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201218_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.DateField(verbose_name='Período')),
            ],
            options={
                'verbose_name_plural': 'Período',
            },
        ),
        migrations.AlterField(
            model_name='setor',
            name='divisao',
            field=models.CharField(choices=[('Têxtil', 'Têxtil'), ('Confecção', 'Confecção')], max_length=20, verbose_name='Divisão'),
        ),
    ]
