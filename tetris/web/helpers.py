#from web.models import Session, Player
import uuid
from datetime import timedelta
from django.utils import timezone


def session_login(username, password):
    from web.models import Session, Player
    try:
        user = Player.objects.get(username=username)
    except Player.DoesNotExist:
        return None

    if user.password != password:
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
    return session.key

GAME_TYPES = [
    ('CL', 'Classic'),
    ('DM', 'Deathmatch'),
    ('TA', 'Time Attack'),
    ('SA', 'Score Attack'),
    ('DR', 'Drag Racing'),
    ('AC', 'Accelerate'),
    ('CF', 'Captue the Flag'),
]


NUMBER_PLAYERS = [
    (1,1),
    (2,2),
    (4,4)
]
