#from web.models import Session, Player
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def session_login(login, password):
    from web.models import Session, Player
    try:
        user = Player.objects.get(login=login)
    except Player.DoesNotExist:
        return None

    if not check_password(password, user.password):
        return None
    session = Session()
    session.key = str(uuid.uuid4())
    session.user = user
    session.expires = timezone.now() + timedelta(days=5)
    session.save()
    return session.key


def auto_login(player):
    from web.models import Session
    session = Session()
    session.key = str(uuid.uuid4())
    session.user = player
    session.expires = timezone.now() + timedelta(days=5)
    session.save()
    print('auto login ', player.login, session.key)
    return session.key

GAME_TYPES = [
    ('CL', 'Classic'),
    ('DM', 'Deathmatch'),
    ('SU', 'Survival'),
    ('LI', 'Lines'),
    ('CO', 'Countdown'),
    ('SA', 'Score Attack'),
    ('DR', 'Drag Racing'),
    ('AC', 'Accelerate'),
    ('CF', 'Capture Flag'),
    ('HF', 'Hold Flag'),
    ('RA', 'Rally')
]


MAX_PLAYERS = 4

TYPE_OF_RESULT = {
'CL': 'score',
'DM': 'score',
'SU': 'time',
'LI': 'time_maxlines',
'CO': 'score_intermediate',
'SA': 'time_climb',
'DR': 'time_drag',
'AC': 'time_acc',
'CF': 'goal',
'HF': 'hold_time',
'RA': 'goal',
}

GAME_COUNTS = {
'CL': 'classic',
'DM': 'deathmatch',
'SU': 'survival',
'LI': 'lines',
'CO': 'countdown',
'SA': 'score',
'DR': 'drag',
'AC': 'acc',
'CF': 'ctf',
'HF': 'hold',
'RA': 'rally',
}

COUNT_STATS = [
'games',
'score',
'time',
'actions',
'lines',
'distance',
'figures',
]

TYPE_STATS = [
'TOTAL',
'CL',
'DM',
'SU',
'LI',
'CO',
'SA',
'DR',
'AC',
'CF',
'HF',
'RA',
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [1, 0, 0], [0, 0, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 0]]
]

POWERUPS = ['chance_up',
            'chance_down',
            'speed_up',
            'speed_down',
            'line_add_1',
            'line_add_2',
            'line_add_3',
            'line_remove_1',
            'line_remove_2',
            'line_remove_3',
            'copy_figure',
            'duration_up',
            'duration_down',
            'thunder',
            'shield',
            'bomb',
            'trash',
            'blind',
            'blind_queue',
            'drink',
            'weak_signal',

            ]

VOLUME_STANDARD = {
    'LI' : 60,
    'CO' : 360,
    'SA' : 20000,
    'DR' : 4020,
    'AC' : 100,
}
