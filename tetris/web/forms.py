import json
import re
from django import forms
from django.db.utils import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.hashers import make_password
from web.models import Player, TetrisRoom
from web.helpers import GAME_TYPES, MAX_PLAYERS


onlychars_validator = RegexValidator(regex=re.compile('^[a-z0-9_]*$',
                                     flags=re.I),
                                     message='Допускаются только буквы \
                                     латинского алфавита(A-Z, a-z), цифры(0-9)\
                                      и знак подчеркивания(_)',
                                     code='invalid',
                                     )

firstchar_validator = RegexValidator(regex=re.compile('^[a-z]',
                                     flags=re.I),
                                     message='Должно начинаться с буквы \
                                     латинского алфавита(A-Z, a-z)',
                                     code='invalid',
                                     )


class SignupForm(forms.Form):
    login = forms.CharField(max_length=20,
                            validators=[onlychars_validator,
                                        firstchar_validator,
                                        MinLengthValidator(
                                            4,
                                            message='Минимум 4 символа')])
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput,
                               validators=[onlychars_validator,
                                           MinLengthValidator(
                                            4,
                                            message='Минимум 4 символа')])

    confirm_password = forms.CharField(max_length=20,
                                       widget=forms.PasswordInput,
                                       validators=[onlychars_validator])

    def clean_login(self):
        input = self.cleaned_data['login']
        if len(Player.objects.filter(login=input)) > 0:
            self.add_error('login',
                           forms.ValidationError(
                            'Такое имя пользователя уже существует. \
                            Выберите другое имя пользователя'))
        return input

    def clean_confirm_password(self):
        input = self.cleaned_data['confirm_password']
        if 'password' not in self.cleaned_data:
            self.add_error('confirm_password',
                           forms.ValidationError(
                            'Пароль не введен либо \
                            не соответствует требованиям'))
        elif input != self.cleaned_data['password']:
            self.add_error('confirm_password',
                           forms.ValidationError(
                            'Пароли не совпадают. \
                            Внимательно введите заново пароль и его повтор'))
        return input

    def save(self):
        del self.cleaned_data['confirm_password']
        new_player = Player(**self.cleaned_data)
        new_player.username = self.cleaned_data['login']
        new_player.password = make_password(self.cleaned_data['password'])
        new_player.save_new()
        return new_player


class LoginForm(forms.Form):
    login = forms.CharField(max_length=20, validators=[onlychars_validator])
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput,
                               validators=[onlychars_validator])

    def clean_login(self):
        input = self.cleaned_data['login']
        return input

    def save(self):
        player = Player.objects.get(login=self.cleaned_data['login'],
                                    password=self.cleaned_data['password'])
        return player


class CreateGameForm(forms.Form):
    possible_players = [(x, x) for x in range(1, MAX_PLAYERS+1)]
    players = forms.ChoiceField(choices=possible_players,
                                widget=forms.RadioSelect)
    game_type = forms.ChoiceField(choices=GAME_TYPES, widget=forms.RadioSelect)
    volume = forms.FloatField(widget=forms.NumberInput(
                                attrs={'min': 25, 'max': 250, 'value': 100}))
    ranked = forms.BooleanField(required=False)
    crazy = forms.BooleanField(required=False)

    def save(self, author):
        cur_room = author.has_room()
        if cur_room is not None:
            return cur_room
        new_room = TetrisRoom()
        new_room.players = int(self.cleaned_data['players'])
        new_room.type = self.cleaned_data['game_type']
        new_room.proc = self.cleaned_data['volume']
        new_room.author = author
        new_room.players_at_positions = json.dumps({x: ""
                                                    for x in range(
                                                        new_room.players)})
        new_room.room_id = TetrisRoom.objects.next_id()
        new_room.ranked = self.cleaned_data['ranked']
        new_room.crazy = self.cleaned_data['crazy']
        new_room.save()
        return new_room
