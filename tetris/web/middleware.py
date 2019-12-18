from web.models import Session, Player
from django.utils import timezone


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            key = request.COOKIES.get('session_key')
            session = Session.objects.get(key=key, expires__gt=timezone.now())
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None

# Code to be executed for each request before
# the view (and later middleware) are called.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
