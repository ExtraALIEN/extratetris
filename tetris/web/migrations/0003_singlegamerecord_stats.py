# Generated by Django 2.2.6 on 2020-03-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_player_li_games'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlegamerecord',
            name='stats',
            field=models.TextField(default=''),
        ),
    ]
