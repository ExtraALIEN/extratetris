# Generated by Django 2.2.6 on 2020-02-20 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20200220_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tetrisroom',
            name='proc',
            field=models.FloatField(default=100.0),
        ),
    ]
