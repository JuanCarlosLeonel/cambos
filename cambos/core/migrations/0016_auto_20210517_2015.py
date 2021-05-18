# Generated by Django 3.0.7 on 2021-05-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_acabamento_oficina_userbot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbot',
            name='acabamento',
            field=models.ManyToManyField(blank=True, to='core.ACABAMENTO'),
        ),
        migrations.AlterField(
            model_name='userbot',
            name='oficina',
            field=models.ManyToManyField(blank=True, to='core.OFICINA'),
        ),
        migrations.AlterField(
            model_name='userbot',
            name='user_tel',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
