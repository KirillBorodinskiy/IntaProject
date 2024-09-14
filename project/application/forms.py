from django import forms
from django.contrib.auth.models import User
from .models import *

class GameCreationForm(forms.ModelForm):
    player_1 = forms.ModelChoiceField(queryset=User.objects.all(), required=True)
    player_2 = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Game
        fields = ['player_1', 'player_2']

class ConnectTablesForm(forms.Form):
    player_1_board = forms.ModelChoiceField(queryset=Board.objects.all(), label='Select Player 1\'s Board')
    player_2_board = forms.ModelChoiceField(queryset=Board.objects.all(), label='Select Player 2\'s Board')

    def clean(self):
        cleaned_data = super().clean()
        player_1_board = cleaned_data.get('player_1_board')
        player_2_board = cleaned_data.get('player_2_board')

        if player_1_board and player_2_board and player_1_board == player_2_board:
            raise forms.ValidationError("Please select two different boards.")

        return cleaned_data