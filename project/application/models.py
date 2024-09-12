import json
from django.db import models

class Game(models.Model):
    player_1 = models.ForeignKey('auth.User', related_name='player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey('auth.User', related_name='player_2', on_delete=models.CASCADE)
    current_turn = models.ForeignKey('auth.User', related_name='current_turn', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Store ship positions as a JSONField directly in the Game model
    ship_positions = models.JSONField(default=list) 

    def initialize_board(self):
        """Инициализация доски 10x10 с пустыми ячейками"""
        board = [['' for _ in range(10)] for _ in range(10)]
        self.board = json.dumps(board)
        self.save()

    def update_cell(self, row, col, value):
        """Обновление состояния ячейки"""
        board = json.loads(self.board)
        board[row][col] = value
        self.board = json.dumps(board)
        self.save()

    def get_board(self):
        """Reconstruct the board based on ship_positions"""
        board = [['' for _ in range(10)] for _ in range(10)]
        for position in self.ship_positions:
            row, col = position['row'], position['column']
            board[row][col] = '1'
        return board