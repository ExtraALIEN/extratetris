from django import forms
from web.models import Player


class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean(self):
        try:
            if Player.objects.get(username=self.cleaned_data['username']):
                raise forms.ValidationError('Выберите другое имя пользователя')
        except Player.DoesNotExist:
            pass


    def save(self):
        new_player = Player(**self.cleaned_data)
        new_player.save()
        return new_player


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def save(self):
        player = Player.objects.get(username=self.cleaned_data['username'],
                                    password=self.cleaned_data['password'])
        return player

NUMBER_PLAYERS = [
    (1,1),
    (2,2),
    (4,4)
]

class CreateGameForm(forms.Form):
    from web.models import GAME_TYPES
    players = forms.ChoiceField(choices=NUMBER_PLAYERS)
    game_type = forms.ChoiceField(choices=GAME_TYPES)
    team_game = forms.BooleanField(required=False)
