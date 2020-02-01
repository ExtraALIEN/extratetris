from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('create-game/', views.create_game),
    path('room/<int:room_number>/', views.enter_room),
    path('room/<int:room_number>/delete/', views.delete_room),
    path('profile/<int:profile_id>/', views.profile),
    path('test/', views.testpage)
]
