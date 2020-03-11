from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from web.forms import SignupForm, LoginForm, CreateGameForm
from web.helpers import session_login, VOLUME_STANDARD
from datetime import timedelta
import time
from django.utils import timezone
from web.models import TetrisRoom, Player

def index(request):
    guest_mode = True
    us = ''
    profile_url = ''
    waiting = False
    cur_room = None
    if request.user and not request.user.is_guest:
        guest_mode = False
        us = request.user.username
        profile_url = request.user.get_url()
        cur_room = request.user.has_room()
        if cur_room is not None:
            waiting = True

    return render(request, 'web/index.html', {'guest_mode': guest_mode,
                                              'user': us,
                                              'profile_url': profile_url,
                                              'waiting' : waiting,
                                              'cur_room' : cur_room
                                              })

def lobby(request):
    rooms = TetrisRoom.objects.all()
    scripts = ['lobbyConnect']
    return render(request, 'web/lobby.html', {'rooms': rooms,
                                              'scripts': scripts
                                              })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            player = form.save()
            redirect = player.do_login()
            return redirect
    else:
        form = SignupForm()
    return render(request, 'web/signup.html', {'form': form})


def login(request):
    error = ""
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        key = session_login(login, password)
        if key:
            response = HttpResponseRedirect('/')
            response.set_cookie('session_key', key,
                                domain='localhost',
                                httponly=True,
                                expires=timezone.now()+timedelta(days=5))
            return response
        else:
            error = "неверный логин/пароль"
            form = LoginForm(request.POST)
    else:
        form = LoginForm(auto_id='%s')
    return render(request, 'web/login.html', {'form': form, 'error': error})


def logout(request):
    current_session = request.session
    if current_session is not None:
        current_session.delete()
    return HttpResponseRedirect('/')


def profile(request, profile_id):
    user = Player.objects.get(pk=profile_id)
    stats = user.get_profile_stats()
    games = user.get_recorded_games()
    scripts = ['profile']
    return render(request, 'web/profile.html', {'stats': stats,
                                                'scripts': scripts,
                                                'games': games})

def create_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            if request.user is None:
                guest = Player.objects.create_guest()
                new_room = form.save(guest)
                url = new_room.get_url()
                return guest.do_login(url=url)
            else:
                new_room = form.save(request.user)
                url = new_room.get_url()
                return HttpResponseRedirect(url)


    else:
        if request.user and request.user.has_room() is not None:
            return HttpResponseRedirect('/')
        form = CreateGameForm(auto_id='id_%s')
        scripts = ['createroom']
    return render(request, 'web/create-game.html', {'form': form,
                                                    'scripts': scripts})


def enter_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(room_id=room_number)
    positions = [x for x in range(room.players)]
    width = [x for x in range(12)]
    height = [x for x in range(25-2,-1,-1)]
    queue = [x for x in range(5)]
    queue_grid = [x for x in range(-1,5)]
    scripts = ['enterroom']
    is_author = False
    if request.user is None:
        guest = Player.objects.create_guest()
        return guest.do_login(room.get_url())
    elif request.user == room.author:
        is_author = True
    limited = room.type in VOLUME_STANDARD
    # if room.started:
    #     scripts = ['gamecontrols']
    return render(request, 'web/room.html', {'room': room,
                                             'positions': positions,
                                             'scripts': scripts,
                                             'width': width,
                                             'height': height,
                                             'queue' : queue,
                                             'queue_grid': queue_grid,
                                             'is_author' : is_author,
                                             'limited' : limited})


def delete_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(room_id=room_number)
    room.delete()
    return HttpResponseRedirect('/')


def play_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(room_id=room_number)
    room.add_player(request.user)
    return HttpResponseRedirect(room.get_url())

def recorded_game(request, game_number):
    from web.models import SingleGameRecord
    game = SingleGameRecord.objects.get(pk=game_number)
    stats = game.load_stats()
    graphs = game.graphs_data()
    scripts = ['record']
    return render(request, 'web/game.html', {'stats': stats,
                                             'data': graphs,
                                             'number': game.pk,
                                             'datestart': game.started_at.strftime('%d %b %Y %H:%I %Z'),
                                             'type': game.type,
                                             'scripts': scripts})

def testpage(request):
    print('test')
    return render(request, 'web/test.html', {})
