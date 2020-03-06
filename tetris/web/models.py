import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
from web.helpers import GAME_TYPES, VOLUME_STANDARD, COUNT_STATS, TYPE_STATS


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
                      username='* anonymous *')
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
    TOTAL_games = models.FloatField(default=0.0)
    TOTAL_eff = models.FloatField(default=0.0)
    TOTAL_score = models.FloatField(default=0.0)
    TOTAL_time = models.FloatField(default=0.0)
    TOTAL_actions = models.FloatField(default=0.0)
    TOTAL_lines = models.FloatField(default=0.0)
    TOTAL_distance = models.FloatField(default=0.0)
    TOTAL_figures = models.FloatField(default=0.0)
    CL_games = models.FloatField(default=0.0)
    CL_eff = models.FloatField(default=0.0)
    CL_score = models.FloatField(default=0.0)
    CL_time = models.FloatField(default=0.0)
    CL_actions = models.FloatField(default=0.0)
    CL_lines = models.FloatField(default=0.0)
    CL_distance = models.FloatField(default=0.0)
    CL_figures = models.FloatField(default=0.0)
    DM_games = models.FloatField(default=0.0)
    DM_eff = models.FloatField(default=0.0)
    DM_score = models.FloatField(default=0.0)
    DM_time = models.FloatField(default=0.0)
    DM_actions = models.FloatField(default=0.0)
    DM_lines = models.FloatField(default=0.0)
    DM_distance = models.FloatField(default=0.0)
    DM_figures = models.FloatField(default=0.0)
    SU_games = models.FloatField(default=0.0)
    SU_eff = models.FloatField(default=0.0)
    SU_score = models.FloatField(default=0.0)
    SU_time = models.FloatField(default=0.0)
    SU_actions = models.FloatField(default=0.0)
    SU_lines = models.FloatField(default=0.0)
    SU_distance = models.FloatField(default=0.0)
    SU_figures = models.FloatField(default=0.0)
    LI_games = models.FloatField(default=0.0)
    LI_eff = models.FloatField(default=0.0)
    LI_score = models.FloatField(default=0.0)
    LI_time = models.FloatField(default=0.0)
    LI_actions = models.FloatField(default=0.0)
    LI_lines = models.FloatField(default=0.0)
    LI_distance = models.FloatField(default=0.0)
    LI_figures = models.FloatField(default=0.0)
    CO_games = models.FloatField(default=0.0)
    CO_eff = models.FloatField(default=0.0)
    CO_score = models.FloatField(default=0.0)
    CO_time = models.FloatField(default=0.0)
    CO_actions = models.FloatField(default=0.0)
    CO_lines = models.FloatField(default=0.0)
    CO_distance = models.FloatField(default=0.0)
    CO_figures = models.FloatField(default=0.0)
    SA_games = models.FloatField(default=0.0)
    SA_eff = models.FloatField(default=0.0)
    SA_score = models.FloatField(default=0.0)
    SA_time = models.FloatField(default=0.0)
    SA_actions = models.FloatField(default=0.0)
    SA_lines = models.FloatField(default=0.0)
    SA_distance = models.FloatField(default=0.0)
    SA_figures = models.FloatField(default=0.0)
    DR_games = models.FloatField(default=0.0)
    DR_eff = models.FloatField(default=0.0)
    DR_score = models.FloatField(default=0.0)
    DR_time = models.FloatField(default=0.0)
    DR_actions = models.FloatField(default=0.0)
    DR_lines = models.FloatField(default=0.0)
    DR_distance = models.FloatField(default=0.0)
    DR_figures = models.FloatField(default=0.0)
    AC_games = models.FloatField(default=0.0)
    AC_eff = models.FloatField(default=0.0)
    AC_score = models.FloatField(default=0.0)
    AC_time = models.FloatField(default=0.0)
    AC_actions = models.FloatField(default=0.0)
    AC_lines = models.FloatField(default=0.0)
    AC_distance = models.FloatField(default=0.0)
    AC_figures = models.FloatField(default=0.0)
    CF_games = models.FloatField(default=0.0)
    CF_eff = models.FloatField(default=0.0)
    CF_score = models.FloatField(default=0.0)
    CF_time = models.FloatField(default=0.0)
    CF_actions = models.FloatField(default=0.0)
    CF_lines = models.FloatField(default=0.0)
    CF_distance = models.FloatField(default=0.0)
    CF_figures = models.FloatField(default=0.0)
    HF_games = models.FloatField(default=0.0)
    HF_eff = models.FloatField(default=0.0)
    HF_score = models.FloatField(default=0.0)
    HF_time = models.FloatField(default=0.0)
    HF_actions = models.FloatField(default=0.0)
    HF_lines = models.FloatField(default=0.0)
    HF_distance = models.FloatField(default=0.0)
    HF_figures = models.FloatField(default=0.0)
    RA_games = models.FloatField(default=0.0)
    RA_eff = models.FloatField(default=0.0)
    RA_score = models.FloatField(default=0.0)
    RA_time = models.FloatField(default=0.0)
    RA_actions = models.FloatField(default=0.0)
    RA_lines = models.FloatField(default=0.0)
    RA_distance = models.FloatField(default=0.0)
    RA_figures = models.FloatField(default=0.0)
    M_TOTAL_games = models.FloatField(default=0.0)
    M_TOTAL_score = models.FloatField(default=0.0)
    M_TOTAL_time = models.FloatField(default=0.0)
    M_TOTAL_actions = models.FloatField(default=0.0)
    M_TOTAL_lines = models.FloatField(default=0.0)
    M_TOTAL_distance = models.FloatField(default=0.0)
    M_TOTAL_figures = models.FloatField(default=0.0)
    M_CL_games = models.FloatField(default=0.0)
    M_CL_score = models.FloatField(default=0.0)
    M_CL_time = models.FloatField(default=0.0)
    M_CL_actions = models.FloatField(default=0.0)
    M_CL_lines = models.FloatField(default=0.0)
    M_CL_distance = models.FloatField(default=0.0)
    M_CL_figures = models.FloatField(default=0.0)
    M_DM_games = models.FloatField(default=0.0)
    M_DM_score = models.FloatField(default=0.0)
    M_DM_time = models.FloatField(default=0.0)
    M_DM_actions = models.FloatField(default=0.0)
    M_DM_lines = models.FloatField(default=0.0)
    M_DM_distance = models.FloatField(default=0.0)
    M_DM_figures = models.FloatField(default=0.0)
    M_SU_games = models.FloatField(default=0.0)
    M_SU_score = models.FloatField(default=0.0)
    M_SU_time = models.FloatField(default=0.0)
    M_SU_actions = models.FloatField(default=0.0)
    M_SU_lines = models.FloatField(default=0.0)
    M_SU_distance = models.FloatField(default=0.0)
    M_SU_figures = models.FloatField(default=0.0)
    M_LI_games = models.FloatField(default=0.0)
    M_LI_score = models.FloatField(default=0.0)
    M_LI_time = models.FloatField(default=0.0)
    M_LI_actions = models.FloatField(default=0.0)
    M_LI_lines = models.FloatField(default=0.0)
    M_LI_distance = models.FloatField(default=0.0)
    M_LI_figures = models.FloatField(default=0.0)
    M_CO_games = models.FloatField(default=0.0)
    M_CO_score = models.FloatField(default=0.0)
    M_CO_time = models.FloatField(default=0.0)
    M_CO_actions = models.FloatField(default=0.0)
    M_CO_lines = models.FloatField(default=0.0)
    M_CO_distance = models.FloatField(default=0.0)
    M_CO_figures = models.FloatField(default=0.0)
    M_SA_games = models.FloatField(default=0.0)
    M_SA_score = models.FloatField(default=0.0)
    M_SA_time = models.FloatField(default=0.0)
    M_SA_actions = models.FloatField(default=0.0)
    M_SA_lines = models.FloatField(default=0.0)
    M_SA_distance = models.FloatField(default=0.0)
    M_SA_figures = models.FloatField(default=0.0)
    M_DR_games = models.FloatField(default=0.0)
    M_DR_score = models.FloatField(default=0.0)
    M_DR_time = models.FloatField(default=0.0)
    M_DR_actions = models.FloatField(default=0.0)
    M_DR_lines = models.FloatField(default=0.0)
    M_DR_distance = models.FloatField(default=0.0)
    M_DR_figures = models.FloatField(default=0.0)
    M_AC_games = models.FloatField(default=0.0)
    M_AC_score = models.FloatField(default=0.0)
    M_AC_time = models.FloatField(default=0.0)
    M_AC_actions = models.FloatField(default=0.0)
    M_AC_lines = models.FloatField(default=0.0)
    M_AC_distance = models.FloatField(default=0.0)
    M_AC_figures = models.FloatField(default=0.0)
    M_CF_games = models.FloatField(default=0.0)
    M_CF_score = models.FloatField(default=0.0)
    M_CF_time = models.FloatField(default=0.0)
    M_CF_actions = models.FloatField(default=0.0)
    M_CF_lines = models.FloatField(default=0.0)
    M_CF_distance = models.FloatField(default=0.0)
    M_CF_figures = models.FloatField(default=0.0)
    M_HF_games = models.FloatField(default=0.0)
    M_HF_score = models.FloatField(default=0.0)
    M_HF_time = models.FloatField(default=0.0)
    M_HF_actions = models.FloatField(default=0.0)
    M_HF_lines = models.FloatField(default=0.0)
    M_HF_distance = models.FloatField(default=0.0)
    M_HF_figures = models.FloatField(default=0.0)
    M_RA_games = models.FloatField(default=0.0)
    M_RA_score = models.FloatField(default=0.0)
    M_RA_time = models.FloatField(default=0.0)
    M_RA_actions = models.FloatField(default=0.0)
    M_RA_lines = models.FloatField(default=0.0)
    M_RA_distance = models.FloatField(default=0.0)
    M_RA_figures = models.FloatField(default=0.0)

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

    def has_room(self):
        if hasattr(self, 'current_room') and self.current_room is not None:
            return self.current_room
        return None

    def update_stats(self, **kwargs):
                     # type=None, multiplayer=False, score=None, time=None,
                     # actions=None, lines=None, distance=None, figures=None,
                     # countdown_score=None, time_lines=None, time_drag=None,
                     # time_climb=None, max_speed=None, games=1):
        types = ['TOTAL', kwargs['type']]
        if kwargs['multiplayer']:
            types.append('M_TOTAL')
            types.append('M_'+ kwargs['type'])
        for x in kwargs:
            if x in COUNT_STATS:
                for t in types:
                    prop = t + '_' + x
                    new_val = getattr(self, prop) +  kwargs[x]
                    setattr(self, prop, new_val)
        self.update_best(**kwargs)
        self.save()

    def update_eff(self, type=None, eff=None):
        self.TOTAL_eff += eff
        prop = type + '_eff'
        new_val = getattr(self, prop) + eff
        setattr(self, prop, new_val)

    def update_best(self, **kwargs):
        if kwargs['score'] and kwargs['score'] > self.best_score:
            self.best_score = kwargs['score']
        if kwargs['countdown_score'] and kwargs['countdown_score'] > self.best_countdown_score:
            self.best_countdown_score = kwargs['countdown_score']
        if not self.best_time_lines or kwargs['time_lines'] and kwargs['time_lines'] < self.best_time_lines:
            self.best_time_lines = kwargs['time_lines']
        if not self.best_time_drag or kwargs['time_drag'] and kwargs['time_drag'] < self.best_time_drag:
            self.best_time_drag = kwargs['time_drag']
        if not self.best_time_climb or kwargs['time_climb'] and kwargs['time_climb'] < self.best_time_climb:
            self.best_time_climb = kwargs['time_climb']
        if not self.best_time_acc or kwargs['time_acc'] and kwargs['time_acc'] < self.best_time_acc:
            self.best_time_acc = kwargs['time_acc']
        if kwargs['time'] and kwargs['time'] > self.best_survival_time:
            self.best_survival_time = kwargs['time']
        if kwargs['max_speed'] and kwargs['max_speed'] > self.best_speed:
            self.best_speed = kwargs['max_speed']
        if kwargs['lines'] and kwargs['lines'] > self.best_lines_count:
            self.best_lines_count = kwargs['lines']
        if kwargs['distance'] and kwargs['distance'] > self.best_distance:
            self.best_distance = kwargs['distance']


    def get_profile_stats(self):
        stats = {
            'user': {
                'outside' : True,
                'username': self.username,
                'date_joined': self.date_joined.strftime('%d %b %Y %H:%I %Z')
                 },
            'best': {
                'outside' : True,
                'speed': round(self.best_speed, 2),
                'score': int(self.best_score),
                'lines': int(self.best_lines_count),
                'distance': int(self.best_distance),
                'survival_time': round(self.best_survival_time/60, 2),
                'time_lines': '-',
                'time_climb': '-',
                'time_drag': '-',
                'time_acc': '-',
                'countdown_score': int(self.best_countdown_score),
                },
            # 'rating': {self.rating},
        }
        if self.best_time_lines:
            stats['best']['time_lines'] = round(self.best_time_lines/60, 2)
        if self.best_time_climb:
            stats['best']['time_climb'] = round(self.best_time_climb/60, 2)
        if self.best_time_drag:
            stats['best']['time_drag'] = round(self.best_time_drag/60, 2)
        if self.best_time_acc:
            stats['best']['time_acc'] = round(self.best_time_acc/60, 2)

        full_stats = COUNT_STATS + ['eff']
        for t in TYPE_STATS:
            dic = {}
            for st in full_stats:
                key = t + '_' + st
                dic[st] = int(getattr(self, key))
            dic['outside'] = False
            dic['score_game'] = '-'
            dic['lines_game'] = '-'
            dic['distance_game'] = '-'
            dic['figures_game'] = '-'
            dic['time_game'] = '-'
            dic['distance_line'] = '-'
            dic['figures_line'] = '-'
            dic['actions_figure'] = '-'
            dic['score_figure'] = '-'
            dic['score_actions'] = '-'
            dic['score_distance'] = '-'
            dic['score_sec'] = '-'
            dic['lines_min'] = '-'
            dic['actions_min'] = '-'
            dic['figures_min'] = '-'
            if dic['games'] > 0:
                dic['score_game'] = round(dic['score']/dic['games'], 2)
                dic['lines_game'] = round(dic['lines']/dic['games'], 2)
                dic['figures_game'] = round(dic['figures']/dic['games'], 2)
                dic['distance_game'] = round(dic['distance']/dic['games'], 2)
                dic['time_game'] = round(dic['time']/dic['games']/60, 2)
            if dic['lines'] > 0:
                dic['distance_line'] = round(dic['distance']/dic['lines'], 2)
                dic['figures_line'] = round(dic['figures']/dic['lines'], 2)
            if dic['figures'] > 0:
                dic['actions_figure'] = round(dic['actions']/dic['figures'], 2)
                dic['score_figure'] = round(dic['score']/dic['figures'], 2)
            if dic['actions'] > 0:
                dic['score_actions'] = round(dic['score']/dic['actions'], 2)
            if dic['distance'] > 0:
                dic['score_distance'] = round(dic['score']/dic['distance'], 2)
            if dic['time'] > 0:
                dic['score_sec'] = round(dic['score']/dic['time'], 2)
                dic['lines_min'] = round(dic['lines']/(dic['time']/60), 2)
                dic['actions_min'] = round(dic['actions']/(dic['time']/60), 2)
                dic['figures_min'] = round(dic['figures']/(dic['time']/60), 2)
                dic['time'] = round(dic['time']/3600, 2)
            del dic['actions']
            del dic['figures']
            stats[t] = dic
        return stats

    def get_recorded_games(self):
        all_games = self.recorded_games.all().order_by('-started_at')
        games = []
        for x in all_games:
            game = {}
            game['started_at'] = x.started_at.strftime('%d %b %Y %H:%I %Z')
            game['type'] = x.type
            game['url'] = x.get_url()
            game['place'] = x.get_place(self)
            games.append(game)
        return games




class SingleGameRecord(models.Model):
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    size = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True)
    positions = models.TextField(default="")
    stats = models.TextField(default="")
    players = models.ManyToManyField(Player, related_name='recorded_games')

    def save_results(self, results):
        self.positions = json.dumps(results)
        self.save()

    def load_results(self):
        return json.loads(self.positions)

    def save_stats(self, stats):
        self.stats = json.dumps(stats)
        self.save()


    def get_url(self):
        return '/results/' + str(self.pk)

    def get_place(self, player):
        places = self.load_results()
        for x in places:
            if player.username in places[x]:
                return x + '/' + str(self.size)


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
    bots = models.IntegerField(default=0)
    botlevels = models.TextField(default="[]")
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    proc = models.FloatField(default=100.0)
    active_players = models.ManyToManyField(Player)
    players_at_positions = models.TextField(default="")
    started = models.BooleanField(default=False)
    start_players = models.TextField(default="")


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

    def add_bot(self, bot, pos):
        self.bots += 1
        pp = json.loads(self.players_at_positions)
        pp[str(pos)] = bot.username
        self.players_at_positions = json.dumps(pp)
        botlevels = json.loads(self.botlevels)
        botlevels.append(bot.level)
        self.botlevels = json.dumps(botlevels)
        self.save()

    def del_bot(self, pos):
        import re
        self.bots -= 1
        pp = json.loads(self.players_at_positions)
        level = re.sub('\D', '', pp[str(pos)])
        pp[str(pos)] = ''
        self.players_at_positions = json.dumps(pp)
        botlevels = json.loads(self.botlevels)
        botlevels.remove(int(level))
        self.botlevels = json.dumps(botlevels)
        self.save()

    def describe(self):
        pp = json.loads(self.players_at_positions)
        info = []
        for x in pp:
            info.append({'pos': x, 'username' : pp[x] or '---'})
        return info




    def get_volume(self):
        print(self.proc)
        if self.type in VOLUME_STANDARD:
            if self.type == 'CO':
                return (self.proc*VOLUME_STANDARD[self.type]) / 100
            return int((self.proc*VOLUME_STANDARD[self.type]) // 100)




    def is_full(self):
        return self.active_players.count() + self.bots == self.players

    def get_url(self):
        return '/room/'+ str(self.room_id)

    def delete_url(self):
        return '/room/'+ str(self.room_id)+'/delete/'

    def start(self):
        self.started = True
        self.start_players = self.players_at_positions
        self.save()
