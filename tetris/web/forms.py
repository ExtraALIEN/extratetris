from django import forms
from web.models import Player, TetrisRoom


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



class CreateGameForm(forms.Form):
    from web.helpers import GAME_TYPES, NUMBER_PLAYERS
    players = forms.ChoiceField(choices=NUMBER_PLAYERS)
    game_type = forms.ChoiceField(choices=GAME_TYPES)
    team_game = forms.BooleanField(required=False)


    def save(self, author):
        # options = {
        #     'players' : self.cleaned_data['players'],
        #     'for_teams' : self.cleaned_data['team_game'],
        #     'author': Player.objects.get(pk=author.pk),
        #     'type' : self.cleaned_data['game_type']
        # }
        new_room = TetrisRoom()
        new_room.players = self.cleaned_data['players']
        new_room.for_teams = self.cleaned_data['team_game']
        new_room.type = self.cleaned_data['game_type']
        new_room.author = author
        new_room.save()
        new_room.add_player(author)


        return new_room
