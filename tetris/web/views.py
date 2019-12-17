from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from web.forms import SignupForm, LoginForm, CreateGameForm
from web.helpers import session_login
from datetime import timedelta
from django.utils import timezone


def detect_user(request):
    return render(request,'web/detect.html',{'user': request.user.username})

def index(request):
    from web.models import TetrisRoom
    text = 'Войдите или зарегистрируйтесь'
    if request.user is not None:
        text = "Добро пожаловать, " + request.user.username
    rooms = TetrisRoom.objects.all()

    return render(request, 'web/index.html', {'text': text, 'rooms': rooms})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            player = form.save()
            redirect = player.login()
            return redirect
    else:
        form = SignupForm()
    return render(request, 'web/signup.html', {'form': form})


def login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        key = session_login(username, password)
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


def create_game(request):
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            new_room = form.save(request.user)
            url = new_room.get_url()
            return HttpResponseRedirect(url)
    else:
        form = CreateGameForm(auto_id='%s')
    return render(request, 'web/create-game.html', {'form': form})


def enter_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(pk=room_number)
    positions = [x for x in range(room.players)]
    scripts = ['enterroom']
    return render(request, 'web/room.html', {'room': room,
                                             'positions': positions,
                                             'scripts': scripts})


def delete_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(pk=room_number)
    room.delete()
    return HttpResponseRedirect('/')


def play_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(pk=room_number)
    room.add_player(request.user)
    return HttpResponseRedirect(room.get_url())


def exit_room(request, room_number):
    from web.models import TetrisRoom
    room = TetrisRoom.objects.get(pk=room_number)
    room.remove_player(request.user)
    return HttpResponseRedirect(room.get_url())
