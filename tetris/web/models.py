import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
from web.helpers import GAME_TYPES, NUMBER_PLAYERS


class PlayerManager(models.Manager):

    def create_guest(self):
        guestcounter = self.filter(is_guest=True).count() + 1
        guest_login = 'guest' + str(guestcounter)
        guest = Player(is_guest=True,
                      login=guest_login,
                      password='',
                      email='guest@extratetris.com',
                      username='anonymous')
        guest.save()
        return guest

class Player(models.Model):
    objects = PlayerManager()
    is_robot = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    login = models.CharField(max_length=20, unique=True)
    password = models.TextField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=1500.0)
    total_score = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    max_speed = models.FloatField(default=0)

    #games =
    #wins =


    def do_login(self, url='/'):
        from web.helpers import auto_login
        from django.http import HttpResponseRedirect
        key = auto_login(self)
        response = HttpResponseRedirect(url)
        response.set_cookie('session_key', key,
                            domain='localhost',
                            httponly=True,
                            expires=timezone.now()+timedelta(days=5))
        return response

    def do_logout(self, request):
        key = request.COOKIES.get('session_key')
        Session.objects.delete(key=key)
        return HttpResponseRedirect('/')




class SingleGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    players = models.ManyToManyField(Player, related_name='user_games')
    winner = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='user_wins')



class Session(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    expires = models.DateTimeField()


class TetrisRoomManager(models.Manager):
    def next_id(self):
        if self.all().count() > 0:
            return self.all().order_by('-pk')[0].pk + 1
        else:
            return 1

class TetrisRoom(models.Model):
    objects = TetrisRoomManager()
    room_id = models.IntegerField(default=0)
    author = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="current_room")
    players = models.IntegerField()
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    active_players = models.ManyToManyField(Player)
    players_at_positions = models.TextField(default="")

    # start_players = models.ManyToManyField(Player, blank=True,null=True)

    def add_player(self, player, pos):
        self.active_players.add(player)
        pp = json.loads(self.players_at_positions)
        pp[str(pos)] = player.username
        self.players_at_positions = json.dumps(pp)
        self.save()


    def remove_player(self, player, pos):
        self.active_players.remove(player)
        pp = json.loads(self.players_at_positions)
        pp[str(pos)] = ''
        self.players_at_positions = json.dumps(pp)
        self.save()

    def count_players(self):
        current = self.active_players.count()
        return str(current) + '/' + str(self.players)

    def is_full(self):
        return self.active_players.count() == self.players

    def get_url(self):
        return '/room/'+ str(self.room_id)

    def delete_url(self):
        return '/room/'+ str(self.room_id)+'/delete/'
