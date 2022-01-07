# Generated by Django 3.2.6 on 2022-01-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frota', '0010_frotapermissao'),
    ]

    operations = [
        migrations.AddField(
            model_name='frotapermissao',
            name='ver_caminhao',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='frotapermissao',
            name='ver_carro',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='frotapermissao',
            name='ver_empilhadeira',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='frotapermissao',
            name='ver_veiculo',
            field=models.BooleanField(default=True),
        ),
    ]
