from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=20)
    rating = models.FloatField()
    joined = models.DateTimeField()


class Player(models.Model):
    name = models.CharField(max_length=20)
    password = models.TextField(max_length=20)
    email = models.EmailField()
    is_robot = models.BooleanField()
    joined = models.DateTimeField()
    rating = models.FloatField()
    total_score = models.IntegerField()
    experience = models.IntegerField()
    max_speed = models.FloatField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True)
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
    players = models.ManyToManyField(Player, blank=True)
    winner = models.ForeignKey(Player, blank=True, on_delete=models.DO_NOTHING)


class TeamGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    teams = models.ManyToManyField(Team, blank=True)
    winner_team = models.ForeignKey(Team, blank=True, on_delete=models.DO_NOTHING)
