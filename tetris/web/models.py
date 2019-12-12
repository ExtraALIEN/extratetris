from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=20)
    rating = models.FloatField()
    joined = models.DateTimeField()


class Player(models.Model):
    username = models.CharField(max_length=20)
    password = models.TextField(max_length=20)
    email = models.EmailField()
    is_robot = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=1500.0)
    total_score = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    max_speed = models.FloatField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    #games =
    #wins =




GAME_TYPES = [
    ('CL', 'Classic'),
    ('DM', 'Deathmatch'),
    ('TA', 'Time Attack'),
    ('SA', 'Score Attack'),
    ('DR', 'Drag Racing'),
    ('AC', 'Accelerate'),
    ('CF', 'Captue the Flag'),
]

class SingleGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    players = models.ManyToManyField(Player, related_name='user_games')
    winner = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='user_wins')


class TeamGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    teams = models.ManyToManyField(Team, related_name='team_games')
    winner_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='team_wins')
