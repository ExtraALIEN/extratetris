# Generated by Django 2.2.6 on 2019-12-28 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20191226_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='tetrisroom',
            name='guests',
            field=models.IntegerField(default=0),
        ),
    ]