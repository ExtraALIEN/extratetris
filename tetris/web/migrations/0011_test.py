# Generated by Django 2.2.6 on 2020-07-13 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_tetrisroom_crazy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_distance', models.IntegerField(default=0)),
            ],
        ),
    ]
