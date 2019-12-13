# Generated by Django 2.2.6 on 2019-12-13 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='TetrisRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('players', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4)])),
                ('type', models.CharField(choices=[('CL', 'Classic'), ('DM', 'Deathmatch'), ('TA', 'Time Attack'), ('SA', 'Score Attack'), ('DR', 'Drag Racing'), ('AC', 'Accelerate'), ('CF', 'Captue the Flag')], max_length=2)),
                ('for_teams', models.BooleanField()),
                ('active_players', models.ManyToManyField(to='web.Player')),
                ('active_teams', models.ManyToManyField(to='web.Team')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_room', to='web.Player')),
            ],
        ),
    ]
