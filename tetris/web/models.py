import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
from web.helpers import GAME_TYPES, NUMBER_PLAYERS


class PlayerManager(models.Manager):

    def create_guest(self):
        guests = self.all().filter(is_guest=True).order_by('-pk')
        if guests:
            last = self.all().filter(is_guest=True).order_by('-pk')[0]
            number = int(last.login[5:]) + 1
            guest_login = 'guest' + str(number)
        else:
            guest_login = 'guest1'
        guest = Player(is_guest=True,
                      login=guest_login,
                      password='',
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
    date_joined = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=1500.0)
    games_count = models.IntegerField(default=0)
    multiplayer_games_count = models.IntegerField(default=0)
    games_count_classic = models.IntegerField(default=0)
    games_count_deathmatch = models.IntegerField(default=0)
    games_count_survival = models.IntegerField(default=0)
    games_count_lines = models.IntegerField(default=0)
    games_count_countdown = models.IntegerField(default=0)
    games_count_score = models.IntegerField(default=0)
    games_count_drag = models.IntegerField(default=0)
    games_count_acc = models.IntegerField(default=0)
    games_count_ctf = models.IntegerField(default=0)
    games_count_rally = models.IntegerField(default=0)
    effective_points = models.FloatField(default=0.0)
    effective_points_classic = models.FloatField(default=0.0)
    effective_points_deathmatch = models.FloatField(default=0.0)
    effective_points_survival = models.FloatField(default=0.0)
    effective_points_lines = models.FloatField(default=0.0)
    effective_points_countdown = models.FloatField(default=0.0)
    effective_points_score = models.FloatField(default=0.0)
    effective_points_drag = models.FloatField(default=0.0)
    effective_points_acc = models.FloatField(default=0.0)
    effective_points_ctf = models.FloatField(default=0.0)
    effective_points_rally = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    time = models.FloatField(default=0.0)
    actions = models.IntegerField(default=0)
    lines = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    figures = models.IntegerField(default=0)
    best_speed = models.FloatField(default=0.0)
    best_score = models.IntegerField(default=0)
    best_distance = models.IntegerField(default=0)
    best_survival_time = models.FloatField(default=0.0)
    best_lines_count = models.IntegerField(default=0)
    best_countdown_score = models.IntegerField(default=0)
    best_time_lines = models.FloatField(null=True, blank=True)
    best_time_climb = models.FloatField(null=True, blank=True)
    best_time_drag = models.FloatField(null=True, blank=True)
    best_time_acc = models.FloatField(null=True, blank=True)



    def do_login(self, url='/'):
        from web.helpers import auto_login
        from django.http import HttpResponseRedirect
        key = auto_login(self)
        response = HttpResponseRedirect(url)
        response.set_cookie('session_key', key,
                            domain='localhost',
                            httponly=True,
                            expires=timezone.now()+timedelta(days=5))
        print('session ', url, key)
        return response

    def do_logout(self, request):
        key = request.COOKIES.get('session_key')
        Session.objects.get(key=key).delete()
        return HttpResponseRedirect('/')

    def get_url(self):
        return '/profile/'+str(self.pk)

    def get_profile_stats(self):
        return '123test'




class SingleGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    size = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True)
    positions = models.TextField(default="")
    players = models.ManyToManyField(Player, related_name='recorded_games')

    def save_results(self, results):
        self.positions = json.dumps(results)
        self.save()

    def load_results(self):
        return json.loads(self.positions)




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
    guests = models.IntegerField(default=0)
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    active_players = models.ManyToManyField(Player)
    players_at_positions = models.TextField(default="")
    started = models.BooleanField(default=False)

    # start_players = models.ManyToManyField(Player, blank=True,null=True)

    def add_player(self, player, pos):
        self.active_players.add(player)
        if player.is_guest:
            self.guests += 1
        pp = json.loads(self.players_at_positions)
        pp[str(pos)] = player.username
        self.players_at_positions = json.dumps(pp)
        self.save()


    def remove_player(self, player, pos):
        self.active_players.remove(player)
        if player.is_guest:
            self.guests -= 1
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

    def start(self):
        self.started = True
        self.save()
