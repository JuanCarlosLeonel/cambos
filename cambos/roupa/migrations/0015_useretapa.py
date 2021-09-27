# Generated by Django 3.1.13 on 2021-09-25 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roupa', '0014_remove_etapa_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEtapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etapa', models.ManyToManyField(blank=True, to='roupa.Etapa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]