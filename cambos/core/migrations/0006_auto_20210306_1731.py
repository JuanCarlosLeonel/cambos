# Generated by Django 3.0.7 on 2021-03-06 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210306_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='comercial',
            field=models.CharField(blank=True, choices=[('Mendes Júnior', 'Mendes Júnior'), ('Xavantes', 'Xavantes'), ('Cotton Move', 'Cotton Move'), ('Geral', 'Geral')], max_length=15, null=True),
        ),
    ]
