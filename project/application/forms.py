from django import forms
from django.contrib.auth.models import User
from .models import *

class ConnectTablesForm(forms.Form):
    player_1_board = forms.ModelChoiceField(
        queryset=Board.objects.filter(in_game=False), 
        label='Select Player 1\'s Board'
    )
    player_2_board = forms.ModelChoiceField(
        queryset=Board.objects.filter(in_game=False), 
        label='Select Player 2\'s Board'
    )
    def clean(self):
        cleaned_data = super().clean()
        player_1_board = cleaned_data.get('player_1_board')
        player_2_board = cleaned_data.get('player_2_board')

        if player_1_board and player_2_board and player_1_board == player_2_board:
            raise forms.ValidationError("Please select two different boards.")
        
        if player_1_board.in_game or player_2_board.in_game:
            raise forms.ValidationError("This board is already in game")
        
        return cleaned_data