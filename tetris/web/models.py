from django.db import models
from django.utils import timezone
from datetime import timedelta
from web.helpers import GAME_TYPES, NUMBER_PLAYERS


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


    def login(self):
        from web.helpers import auto_login
        from django.http import HttpResponseRedirect
        key = auto_login(self)
        response = HttpResponseRedirect('/')
        response.set_cookie('session_key', key,
                            domain='localhost',
                            httponly=True,
                            expires=timezone.now()+timedelta(days=5))
        return response

    def logout(self, request):
        key = request.COOKIES.get('session_key')
        Session.objects.delete(key=key)
        return HttpResponseRedirect('/')


class SingleGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    players = models.ManyToManyField(Player, related_name='user_games')
    winner = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='user_wins')


class TeamGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    teams = models.ManyToManyField(Team, related_name='team_games')
    winner_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='team_wins')


class Session(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    expires = models.DateTimeField()


class TetrisRoom(models.Model):
    author = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="current_room")
    players = models.IntegerField()
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    for_teams = models.BooleanField()
    active_players = models.ManyToManyField(Player, blank=True,null=True)
    active_teams = models.ManyToManyField(Team,blank=True,null=True)

    def add_player(self, player):
        self.active_players.add(player)
        if self.is_full():
            self.start_game()

    def remove_player(self, player):
        self.active_players.remove(player)

    def count_players(self):
        current = self.active_players.count()
        return str(current) + '/' + str(self.players)

    def is_full(self):
        return self.active_players.count() == self.players

    def get_url(self):
        return '/room/'+ str(self.pk)

    def delete_url(self):
        return '/room/'+ str(self.pk)+'/delete/'

    def play_url(self):
        return '/room/'+ str(self.pk)+'/play/'

    def exit_url(self):
        return '/room/'+ str(self.pk)+'/exit/'

    def start_game(self):
        pass
