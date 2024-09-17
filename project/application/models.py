import json
from django.db import models

class Board(models.Model):
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ship_positions = models.TextField(default="")
    in_game = models.BooleanField(default=False)


class Game(models.Model):
    player_1 = models.ForeignKey('auth.User', related_name='games_as_player1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey('auth.User', related_name='games_as_player2', on_delete=models.CASCADE)
    player_1_board = models.ForeignKey(Board, related_name='games_as_player1_board', on_delete=models.CASCADE,default=1)
    player_2_board = models.ForeignKey(Board, related_name='games_as_player2_board', on_delete=models.CASCADE,default=1)
    current_turn = models.ForeignKey('auth.User', related_name='current_turn_games', on_delete=models.CASCADE)
    winner = models.ForeignKey('auth.User', related_name='winner', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_board(self):

        player_1_board = self.player_1_board
        player_2_board = self.player_2_board

        board_1 = player_1_board.ship_positions
        board_2 = player_2_board.ship_positions

        return {'player_1': board_1, 'player_2': board_2}