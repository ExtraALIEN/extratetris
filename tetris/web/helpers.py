from web.models import Session, Player
import uuid
from datetime import timedelta
from django.utils import timezone

def session_login(username,password):
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
