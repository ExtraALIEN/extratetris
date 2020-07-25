import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
from web.helpers import GAME_TYPES, VOLUME_STANDARD, \
                        COUNT_STATS, TYPE_STATS, TYPE_OF_BEST, LIST_BEST, \
                        BEST_UPDATE, DIC_STATS, DIC_DIVIDES


class PlayerRecordMetaclass(models.base.ModelBase):

    def __new__(cls, name, bases, attrs):
        for stat in LIST_BEST:
            att = f'best_{stat}_REC'
            attrs[att] = models.ForeignKey('SingleGameRecord',
                                           blank=True, null=True,
                                           on_delete=models.SET_NULL,
                                           related_name=att)
        clsobj = super().__new__(cls, name, bases, attrs)
        return clsobj


class PlayerRecord(models.Model, metaclass=PlayerRecordMetaclass):
    pass


class PlayerManager(models.Manager):

    def create_guest(self):
        guests = self.all().filter(is_guest=True).order_by('-pk')
        if guests:
            last = self.all().filter(is_guest=True).order_by('-pk')[0]
            number = int(last.login[5:]) + 1
            guest_login = f'guest{str(number)}'
        else:
            guest_login = 'guest1'
        guest = Player(is_guest=True,
                       login=guest_login,
                       password='',
                       username='* anonymous *')
        guest.save()
        return guest

    def get_top(self, mode, max_number=100):
        reverse_types = ['']
        prop = ''
        games = 'TOTAL_games'
        if len(mode) == 2:
            prop = f'{mode}_rating'
            games = f'M_{mode}_games'
        elif mode == 'hours':
            prop = 'TOTAL_time'
        else:
            prop = f'best_{mode}'
        ord = prop
        if not mode.startswith('time_'):
            ord = f'-{prop}'
        top_players = list(self.all()
                               .exclude(**{f'{prop}__isnull': True})
                               .order_by(ord))[:max_number]
        data = [{'pos': top_players.index(x) + 1,
                 'username': x.username,
                 'url': x.get_url(),
                 'result': getattr(x, prop),
                 'games': getattr(x, games)} for x in top_players]
        return data


class PlayerMetaclass(models.base.ModelBase):

    def __new__(cls, name, bases, attrs):
        for type in TYPE_STATS:
            for stat in COUNT_STATS:
                att = f'{type}_{stat}'
                m_att = f'M_{att}'
                attrs[att] = models.FloatField(default=0.0)
                attrs[m_att] = models.FloatField(default=0.0)
            e_att = f'{type}_eff'
            attrs[e_att] = models.FloatField(default=0.0)
            if type != 'TOTAL':
                r_att = f'{type}_rating'
                attrs[r_att] = models.FloatField(default=1500.0)
        clsobj = super().__new__(cls, name, bases, attrs)
        return clsobj


class Player(models.Model, metaclass=PlayerMetaclass):
    objects = PlayerManager()
    is_guest = models.BooleanField(default=False)
    login = models.CharField(max_length=20, unique=True)
    password = models.TextField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)
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
    record_card = models.OneToOneField(PlayerRecord,
                                       null=True, blank=True,
                                       on_delete=models.CASCADE)

    def save_new(self):
        record = PlayerRecord()
        record.save()
        self.record_card = record
        self.save()

    def do_login(self, url='/'):
        from django.http import HttpResponseRedirect
        from web.helpers import auto_login
        key = auto_login(self)
        response = HttpResponseRedirect(url)
        response.set_cookie('session_key', key,
                            # domain='localhost',
                            httponly=True,
                            expires=timezone.now()+timedelta(days=5))
        return response

    def do_logout(self, request):
        key = request.COOKIES.get('session_key')
        Session.objects.get(key=key).delete()
        return HttpResponseRedirect('/')

    def get_url(self):
        return f'/profile/{str(self.pk)}'

    def has_room(self):
        if hasattr(self, 'current_room') and self.current_room is not None:
            return self.current_room
        return None

    def update_stats(self, **kwargs):
        # type=None, rec=None, multiplayer=False, score=None, time=None,
        # actions=None, lines=None, distance=None, figures=None,
        # countdown_score=None, time_lines=None, time_drag=None,
        # time_climb=None, max_speed=None, games=1):
        types = ['TOTAL', kwargs['type']]
        if kwargs['multiplayer']:
            types.append('M_TOTAL')
            types.append(f'M_{kwargs["type"]}')
        for x in kwargs:
            if x in COUNT_STATS:
                for t in types:
                    prop = f'{t}_{x}'
                    new_val = getattr(self, prop) + kwargs[x]
                    setattr(self, prop, new_val)
        self.update_best(**kwargs)
        self.save()

    def update_eff(self, type=None, eff=None):
        self.TOTAL_eff += eff
        prop = f'{type}_eff'
        new_val = getattr(self, prop) + eff
        setattr(self, prop, new_val)

    def update_rating(self, type, delta):
        prop = f'{type}_rating'
        new_rating = round(getattr(self, prop) + delta)
        setattr(self, prop, new_rating)

    def update_best(self, **kwargs):

        def update_record(res, prop):
            setattr(self, prop, res)
            setattr(self.record_card, f'{prop}_REC', kwargs['rec'])

        for stat in BEST_UPDATE:
            res = kwargs[stat]
            if res:
                prop = f'best_{BEST_UPDATE[stat]}'
                cur = getattr(self, prop)
                if cur is None:
                    update_record(res, prop)
                elif stat.startswith('time_'):
                    if res < cur:
                        update_record(res, prop)
                elif res > cur:
                    update_record(res, prop)
        self.record_card.save()

    def get_profile_stats(self):
        stats = {
            'user': {
                'outside': True,
                'username': self.username,
                'date_joined': self.date_joined.strftime('%d %b %Y %H:%I %Z')
                 },
            'best': {
                'outside': True,
                'speed': round(self.best_speed, 2),
                'score': int(self.best_score),
                'lines': int(self.best_lines_count),
                'distance': int(self.best_distance),
                'survival_time': round(self.best_survival_time),
                'time_lines': '-',
                'time_climb': '-',
                'time_drag': '-',
                'time_acc': '-',
                'countdown_score': int(self.best_countdown_score),
                }
        }
        for x in ['lines', 'climb', 'drag', 'acc']:
            att = f'best_time_{x}'
            cur = getattr(self, att)
            if cur:
                stat = f'time_{x}'
                stats['best'][stat] = round(cur/60, 2)
        full_stats = COUNT_STATS + ['eff'] + ['rating']
        for t in TYPE_STATS:
            dic = {}
            for st in full_stats:
                key = f'{t}_{st}'
                if t == 'TOTAL' and st == 'rating':
                    continue
                dic[st] = float(getattr(self, key))
                if st == 'eff':
                    games_key = f'M_{t}_games'
                    games = int(getattr(self, games_key))
                    if games > 0:
                        dic[st] = round(dic[st]/games, 2)
            dic['outside'] = False
            for x in DIC_STATS:
                for stat in DIC_STATS[x]:
                    att = f'{stat}_{x}'
                    dic[att] = '-'
            for x in DIC_DIVIDES:
                for stat in DIC_STATS[DIC_DIVIDES[x]]:
                    if dic[x] > 0:
                        att = f'{stat}_{DIC_DIVIDES[x]}'
                        dic[att] = dic[stat]/dic[x]
            if dic['time'] > 0:
                dic['score_sec'] = dic['score']/dic['time']
                dic['lines_min'] = dic['lines']/(dic['time']/60)
                dic['actions_min'] = dic['actions']/(dic['time']/60)
                dic['figures_min'] = dic['figures']/(dic['time']/60)
                dic['time'] = dic['time']/3600
            del dic['actions']
            del dic['figures']
            for x in dic:
                val = dic[x]
                if isinstance(val, float):
                    if val % 1 == 0:
                        dic[x] = int(val)
                    else:
                        dic[x] = round(val, 2)
            stats[t] = dic

        return stats

    def get_recorded_games(self):
        all_games = self.recorded_games.all().order_by('-started_at')[:50]
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
    graphs = models.TextField(default="")
    players = models.ManyToManyField(Player, related_name='recorded_games')

    def save_results(self, results):
        self.positions = json.dumps(results)
        self.save()

    def load_results(self):
        return json.loads(self.positions)

    def save_stats(self, stats):
        stats_to_base = {}
        for x in stats:
            stats_to_base[x] = {}
            for key in stats[x]:
                new_key = key.replace('-', '_')
                val = stats[x][key]
                if key in ['username']:
                    stats_to_base[x][new_key] = val
                elif val:
                    val = float(val)
                    if val % 1 != 0:
                        stats_to_base[x][new_key] = round(val, 2)
                    else:
                        stats_to_base[x][new_key] = int(val)
                else:
                    stats_to_base[x][new_key] = '-'
        self.stats = json.dumps(stats_to_base)
        self.save()

    def save_graphs(self, graphs):
        data = {}
        for x in graphs:
            data[x] = {}
            for stat in ['score', 'lines', 'speed', 'distance', 'figures']:
                data[x][stat] = {
                                 'times': [0],
                                 'vals': [0]
                                 }
            for time in graphs[x]:
                for stat in graphs[x][time]:
                    data[x][stat]['times'].append(time)
                    data[x][stat]['vals'].append(graphs[x][time][stat])
        self.graphs = json.dumps(data)
        self.save()

    def graphs_data(self):
        data = {'game': json.loads(self.graphs),
                'last': self.graph_last10_player()
                }
        if self.type in TYPE_OF_BEST:
            data['best'] = self.best_graphs()
        return data

    def best_graphs(self):
        stats = self.load_stats()
        names = {stats[x]['username']: x for x in stats.keys()}
        graphs = {}
        for player in self.players.all():
            rec = player.record_card
            name = player.username.replace('_', '-')
            pos = names[name]
            prop = 'best_' + TYPE_OF_BEST[self.type] + '_REC'
            graphs[pos] = getattr(rec, prop).graph_of_player(name)
        return graphs

    def graph_of_player(self, username):
        stats = self.load_stats()
        names = {stats[x]['username']: x for x in stats.keys()}
        pos = names[username]
        return json.loads(self.graphs)[pos]

    def graph_last10_player(self):
        stats = self.load_stats()
        names = [stats[x]['username'] for x in stats.keys()]
        players = []
        for name in names:
            players.append(Player.objects
                                 .filter(username=name.replace('_', '-')))
        games = {}
        for x in range(len(players)):
            if players[x].count() == 1:
                games[x] = players[x][0] \
                           .recorded_games \
                           .filter(type=self.type) \
                           .order_by('-started_at')[:10]
        data = {}
        for x in games:
            data[x] = {'speed': [0],
                       'score': [0],
                       'distance': [0],
                       'figures': [0],
                       'lines': [0],
                       'max_times': [],
                       }
            summary = [game.graph_of_player(names[x]) for game in games[x]]
            max_time = int(max([max([graph[stat]['times'][-1]
                           for stat in graph])
                           for graph in summary])) + 1
            for graph in summary:
                cur_max_time = int(max([graph[stat]['times'][-1]
                                   for stat in graph])) + 1
                data[x]['max_times'].append(cur_max_time)
                for stat in graph:
                    stat_max_time = int(graph[stat]['times'][-1]) + 1
                    pos = 0
                    for time in range(stat_max_time):
                        while graph[stat]['times'][pos] < \
                              time < graph[stat]['times'][-1]:
                            pos += 1
                        t = graph[stat]['times'][pos]
                        v = graph[stat]['vals'][pos]
                        if time > len(data[x][stat]) - 1:
                            data[x][stat].append(0)
                        if time != int(t):
                            v = graph[stat]['vals'][pos-1]
                        data[x][stat][time] += v
                    for time in range(stat_max_time, max_time):
                        if time > len(data[x][stat]) - 1:
                            data[x][stat].append(0)
                        data[x][stat][time] += graph[stat]['vals'][-1]
        return data

    def get_url(self):
        return f'/results/{str(self.pk)}'

    def get_place(self, player):
        places = self.load_results()
        for x in places:
            if player.username in places[x]:
                return f'{x}/{str(self.size)}'

    def load_stats(self):
        return json.loads(self.stats)


class Session(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(Player, blank=True,
                             null=True, on_delete=models.CASCADE)
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
    author = models.OneToOneField(Player, on_delete=models.CASCADE,
                                  related_name="current_room")
    players = models.IntegerField()
    guests = models.IntegerField(default=0)
    bots = models.IntegerField(default=0)
    botlevels = models.TextField(default="[]")
    type = models.CharField(max_length=2, choices=GAME_TYPES)
    ranked = models.BooleanField(default=False)
    crazy = models.BooleanField(default=False)
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
        if self.ranked:
            rateprop = f'{self.type}_rating'
            pp[str(pos)] += f':{str(round(getattr(player, rateprop)))}'
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
        if self.ranked:
            pp[str(pos)] += f':{str(bot.rating)}'
        self.players_at_positions = json.dumps(pp)
        botlevels = json.loads(self.botlevels)
        botlevels.append(bot.level)
        self.botlevels = json.dumps(botlevels)
        self.save()

    def del_bot(self, pos):
        import re
        self.bots -= 1
        pp = json.loads(self.players_at_positions)
        botinfo = pp[str(pos)]
        if self.ranked:
            botinfo = botinfo.split(':')[0]
        level = re.sub(r'\D', '', botinfo)
        pp[str(pos)] = ''
        self.players_at_positions = json.dumps(pp)
        botlevels = json.loads(self.botlevels)
        botlevels.remove(int(level))
        self.botlevels = json.dumps(botlevels)
        self.save()

    def describe(self):
        pl = self.players_at_positions
        if self.started:
            pl = self.start_players
        pp = json.loads(pl)
        info = []
        for x in pp:
            info.append({'pos': x, 'username': pp[x] or '---'})
        return info

    def get_volume(self):
        if self.type in VOLUME_STANDARD:
            if self.type == 'CO':
                return (self.proc*VOLUME_STANDARD[self.type]) / 100
            return int((self.proc*VOLUME_STANDARD[self.type]) // 100)

    def is_full(self):
        return self.active_players.count() + self.bots == self.players

    def get_url(self):
        return f'/room/{str(self.room_id)}'

    def delete_url(self):
        return f'/room/{str(self.room_id)}/delete/'

    def start(self):
        self.started = True
        self.start_players = self.players_at_positions
        self.save()
