from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Index")

def login(request):
    return HttpResponse("Login")

def signup(request):
    return HttpResponse("Signup")

def lobby(request):
    return HttpResponse("Lobby")
