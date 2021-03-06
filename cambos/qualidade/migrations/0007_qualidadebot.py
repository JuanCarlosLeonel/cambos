# Generated by Django 3.2.6 on 2022-03-20 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roupa', '0002_fichacorte'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qualidade', '0006_auto_20220319_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='QualidadeBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
                ('user_nome', models.CharField(max_length=30)),
                ('ativo', models.BooleanField(default=True)),
                ('pedido_parado', models.ManyToManyField(blank=True, to='roupa.Etapa')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
