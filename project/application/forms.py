from django import forms
from django.contrib.auth.models import User
from .models import Game

class GameCreationForm(forms.ModelForm):
    player_1 = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    player_2 = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Game
        fields = ['player_1', 'player_2']