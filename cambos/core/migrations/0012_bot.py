# Generated by Django 3.0.7 on 2021-05-15 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210502_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update_id', models.CharField(max_length=30)),
                ('token', models.CharField(max_length=30)),
            ],
        ),
    ]
