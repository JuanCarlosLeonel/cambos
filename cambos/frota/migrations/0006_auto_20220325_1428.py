# Generated by Django 3.2.6 on 2022-03-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0005_auto_20220325_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='frotapermissao',
            name='ver_gerador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='frotapermissao',
            name='ver_trator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='gerador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='veiculo',
            name='trator',
            field=models.BooleanField(default=False),
        ),
    ]