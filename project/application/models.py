import json
from django.db import models

class Game(models.Model):
    board = models.TextField()
    player_1 = models.ForeignKey('auth.User', related_name='player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey('auth.User', related_name='player_2', on_delete=models.CASCADE)
    current_turn = models.ForeignKey('auth.User', related_name='current_turn', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        """Получить текущее состояние доски в виде двумерного массива"""
        return json.loads(self.board)
    
class ShipPosition(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()

    def __str__(self):
        return f"Row: {self.row}, Column: {self.column}"