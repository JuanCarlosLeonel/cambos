# Generated by Django 3.2 on 2022-01-13 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roupa', '0021_alter_roupabot_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='roupabot',
            name='frota',
            field=models.BooleanField(default=False),
        ),
    ]
