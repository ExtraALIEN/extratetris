from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from web.forms import SignupForm, LoginForm
from web.helpers import session_login
from datetime import timedelta
from django.utils import timezone


def index(request):
    player = request.user.username
    return render(request, 'web/index.html', {'player': player})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
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
