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
    scripts = ['index']
    print('render start')
    return render(request, 'web/index.html', {'guest_mode': guest_mode,
                                              'user': us,
                                              'profile_url': profile_url,
                                              'waiting' : waiting,
                                              'cur_room' : cur_room,
                                              'scripts': scripts
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
        form = LoginForm(request.POST)
        if form.is_valid():
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
        else:
            error = 'некорректно введен логин/пароль'
    else:
        form = LoginForm(auto_id='%s')
    return render(request, 'web/login.html', {'form': form, 'error': error})


def logout(request):
    current_session = request.session
    if current_session is not None:
        current_session.delete()
    return HttpResponseRedirect('/')


def profile(request, profile_id):
    try:
        user = Player.objects.get(pk=profile_id)
        stats = user.get_profile_stats()
        games = user.get_recorded_games()
        scripts = ['profile']
        return render(request, 'web/profile.html', {'stats': stats,
                                                    'scripts': scripts,
                                                    'games': games})
    except Player.DoesNotExist:
        return HttpResponseRedirect('/')

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
        guest_mode = request.user is None or request.user.is_guest
    return render(request, 'web/create-game.html', {'form': form,
                                                    'scripts': scripts,
                                                    'guest_mode': guest_mode})


def enter_room(request, room_number):
    from web.models import TetrisRoom
    try:
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
        time_result = ['SU']
        guest_mode = request.user.is_guest
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
                                                 'guest_mode': guest_mode,
                                                 'limited' : limited,
                                                 'time_result' : room.type in time_result})
    except TetrisRoom.DoesNotExist:
        return HttpResponseRedirect('/')


def delete_room(request, room_number):
    from web.models import TetrisRoom
    if request.user and request.user.username == 'extraalien':
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
    try:
        game = SingleGameRecord.objects.get(pk=game_number)
        stats = game.load_stats()
        graphs = game.graphs_data()
        scripts = ['record']
        return render(request, 'web/game.html', {'stats': stats,
                                                 'data': graphs,
                                                 'number': game.pk,
                                                 'datestart': game.started_at.strftime('%d %b %Y %H:%I %Z'),
                                                 'type': game.type,
                                                 'result_is_time': game.type in ['SU'],
                                                 'scripts': scripts})
    except SingleGameRecord.DoesNotExist:
        return HttpResponseRedirect('/')

def top_results(request, mode='score'):
    types = {'CL': 'Classic',
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
    if mode in types:
        players = Player.objects.get_top(mode=mode)
        scripts = ['top']
        return render(request, 'web/top.html', {'mode': mode,
                                            'type_mode': types[mode],
                                            'players': players,
                                            'types': types,
                                            'scripts': scripts})
    return HttpResponseRedirect('/')


def testpage(request):
    print('test')
    return render(request, 'web/test.html', {})
