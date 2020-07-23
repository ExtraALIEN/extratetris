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

TOP_TYPES = {'CL': 'Classic',
             'DM': 'Deathmatch',
             'SU': 'Survival',
             'LI': 'Lines',
             'CO': 'Countdown',
             'SA': 'Score Attack',
             'DR': 'Drag Racing',
             'AC': 'Accelerate',
             'CF': 'Capture Flag',
             'HF': 'Hold Flag',
             'RA': 'Rally',
             'speed': 'Максимальная скорость',
             'score': 'Очков в 1 игре',
             'lines_count': 'Линий в 1 игре',
             'distance': 'Пробег в 1 игре',
             'survival_time': 'Время выживания',
             'time_acc': 'Разгон до 100',
             'time_lines': 'Время 60 линий',
             'time_drag': 'Время 4020 шагов',
             'time_climb': 'Время 20000 очков',
             'countdown_score': 'Очки за 6 минут',
             'hours': 'Часов в игре'
             }

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

TYPE_OF_BEST = {
    'CL': 'score',
    'DM': 'score',
    'SU': 'survival_time',
    'LI': 'time_lines',
    'CO': 'countdown_score',
    'SA': 'time_climb',
    'DR': 'time_drag',
    'AC': 'time_acc',
}

LIST_BEST = [
    'speed',
    'score',
    'distance',
    'survival_time',
    'lines_count',
    'countdown_score',
    'time_lines',
    'time_climb',
    'time_drag',
    'time_acc'
]

BEST_UPDATE = {
    'max_speed': 'speed',
    'score': 'score',
    'distance': 'distance',
    'time': 'survival_time',
    'lines': 'lines_count',
    'countdown_score': 'countdown_score',
    'time_lines': 'time_lines',
    'time_climb': 'time_climb',
    'time_drag': 'time_drag',
    'time_acc': 'time_acc'
}

DIC_STATS = {
    'game': ['score', 'lines', 'distance', 'figures', 'time'],
    'line': ['distance', 'figures'],
    'figure': ['actions', 'score'],
    'actions': ['score'],
    'distance': ['score'],
    'sec': ['score'],
    'min': ['lines', 'actions', 'figures']
}

DIC_DIVIDES = {
    'games': 'game',
    'lines': 'line',
    'figures': 'figure',
    'actions': 'actions',
    'distance': 'distance'
}

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
    'LI': 60,
    'CO': 360,
    'SA': 20000,
    'DR': 4020,
    'AC': 100,
}

BOT_RATINGS = {
    'CL': [438, 710, 857, 1077, 1197,
           1236, 1275, 1314, 1341, 1380,
           1500, 1520, 1559, 1991, 2111,
           2231, 2248, 2287, 2337, 2555, 2582],
    'DM': [0, 0, 185, 546, 585,
           946, 1164, 1184, 1204, 1243,
           1422, 1461, 1500, 1539, 1601,
           1618, 1657, 1677, 1694, 1814, 1934],
    'SU': [309, 353, 392, 419, 458,
           485, 605, 610, 619, 658,
           1019, 1380, 1500, 1620, 1811,
           1825, 1945, 2163, 2283, 2644, 2651],
    'LI': [0, 0, 0, 0, 0, 0,
           95, 134, 300, 420, 586,
           804, 924, 1142, 1262, 1382,
           1461, 1500, 1861, 1981, 2020],
    'CO': [0, 0, 0, 0, 0, 0,
           0, 0, 0, 53, 271,
           489, 609, 614, 676, 1014,
           1019, 1139, 1500, 1527, 1544],
    'SA': [87, 87, 87, 87, 87,
           126, 203, 421, 701, 721,
           726, 944, 1162, 1282, 1500,
           1620, 1678, 1717, 1822, 1833, 1953],
    'DR': [202, 202, 202, 202, 241,
           320, 486, 525, 564, 782,
           902, 981, 1101, 1140, 1260,
           1380, 1500, 1620, 1740, 2101, 2221],
    'AC': [0, 0, 0, 0, 0, 0,
           0, 0, 103, 142, 221,
           582, 842, 1203, 1282, 1500,
           1539, 1559, 1589, 1628, 1667],
    'CF': [865, 865, 944, 973, 1012,
           1051, 1130, 1169, 1174, 1193,
           1232, 1398, 1411, 1421, 1500,
           1539, 1571, 1650, 1729, 1806, 1833],
    'HF': [277, 484, 489, 541, 546,
           625, 651, 677, 696, 715,
           754, 874, 879, 958, 1319,
           1439, 1444, 1483, 1500, 1505, 1625],
    'RA': [917, 927, 1093, 1112, 1151,
           1156, 1164, 1284, 1303, 1322,
           1401, 1500, 1620, 1659, 1802,
           1922, 2042, 2162, 2282, 2402, 2522]
}
