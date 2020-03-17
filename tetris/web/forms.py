from django import forms
from web.models import Player, TetrisRoom
from web.helpers import GAME_TYPES, MAX_PLAYERS
import json
from django.db.utils import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean(self):
        if len(Player.objects.filter(login=self.cleaned_data['login'])) == 0:
            try:
                validate_password(self.cleaned_data['password'])
            except ValidationError as error:
                self.add_error('password', forms.ValidationError('Пароль должен быть не менее 6 символов, \
                 состоять из букв и цифр латинского алфавита'))
        else:
            self.add_error('login', forms.ValidationError('Такое имя пользователя уже существует. \
             Выберите другое имя пользователя'))





    def save(self):
        new_player = Player(**self.cleaned_data)
        new_player.username = self.cleaned_data['login']
        new_player.save()
        return new_player


class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def save(self):
        player = Player.objects.get(login=self.cleaned_data['login'],
                                    password=self.cleaned_data['password'])
        return player



class CreateGameForm(forms.Form):
    possible_players = [(x,x) for x in range(1, MAX_PLAYERS+1)]
    players = forms.ChoiceField(choices=possible_players, widget=forms.RadioSelect)
    game_type = forms.ChoiceField(choices=GAME_TYPES, widget=forms.RadioSelect)
    volume = forms.FloatField(widget=forms.NumberInput(attrs={'min': 25, 'max': 250, 'value': 100}))

    def save(self, author):
        cur_room = author.has_room()
        if cur_room is not None:
            return cur_room
        new_room = TetrisRoom()
        new_room.players = int(self.cleaned_data['players'])
        new_room.type = self.cleaned_data['game_type']
        new_room.proc = self.cleaned_data['volume']
        new_room.author = author
        new_room.players_at_positions = json.dumps({x: "" for x in range(new_room.players)})
        new_room.room_id = TetrisRoom.objects.next_id()
        new_room.save()



        return new_room
