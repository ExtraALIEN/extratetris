from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('lobby/', views.lobby),
    path('create-game/', views.create_game),
    path('room/<int:room_number>/', views.enter_room),
    path('room/<int:room_number>/delete/', views.delete_room),
    path('profile/<int:profile_id>/', views.profile),
    path('results/<int:game_number>/', views.recorded_game),
    path('test/', views.testpage)
]
