# Generated by Django 3.2.6 on 2021-12-21 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0028_pessoa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motorista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnh', models.CharField(max_length=20)),
                ('nome', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.pessoa')),
            ],
            options={
                'db_table': 'frota"."motorista',
            },
        ),
    ]