from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Game
from .forms import GameCreationForm
from django.http import JsonResponse
import json
from .forms import ConnectTablesForm


def connect_tables(request):
    if request.method == 'POST':
        form = ConnectTablesForm(request.POST)
        if form.is_valid():
            player_1_board = form.cleaned_data['player_1_board']
            player_2_board = form.cleaned_data['player_2_board']

            # Create a new Game instance and associate the boards
            game = Game.objects.create(
                player_1=player_1_board.player_1,  # Assuming player_1 is associated with the board
                player_2=player_2_board.player_1,  # Assuming player_1 is associated with the board
                current_turn=player_1_board.player_1,  # You might want to choose the starting player differently
            )

            # You might want to update the original boards to indicate they're now part of a game
            player_1_board.in_game = True
            player_1_board.save()
            player_2_board.in_game = True
            player_2_board.save()

            return render('game_view', game_id=game.id)
    else:
        form = ConnectTablesForm()

    return render(request, 'connect-tables.html', {'form': form})


def index(request):
    return HttpResponse("haha")

def create_game(request):
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            # Установите текущего игрока, если необходимо
            game.current_turn = game.player_1  # Пример установки начального хода
            game.save()
            return redirect('create_board', game_id=game.id)  # Pass game_id as a keyword argument
    else:
        form = GameCreationForm()
    return render(request, 'create-game.html', {'form': form})


def create_board(request,game_id):
    # Create an empty 10x10 board as a dictionary
    board = {row_index: {col_index: '' for col_index in range(10)} for row_index in range(10)}

    ShipList = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    request.session['game_id'] = game_id

    return render(request, 'create-board.html', {'board': board, 'ShipList': ShipList})

def board_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    board = game.get_board()  # Use the get_board method to reconstruct the board
    return render(request, 'application/board.html', {'board': board})

def board(request):
    r = range(11)
    n = [0,1,2,3,4,5,6,7,8,9,10]
    l = ['Z','A','B','C','D','E','F','G','H','I','J']
    rn = list(zip(r, n))
    rl = list(zip(r, l))
    context = {
        'rn': rn,
        'rl': rl,
        'zi': list(zip(r,n,l)),
        'range':r,
    }
    return render(request, 'application/board.html',context)

def board_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    board = game.get_board()
    return render(request, 'board.html', {'board': board})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def add_ship_position(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            row = data.get('row')
            column = data.get('column')

            if row is not None and column is not None:
                # Save the ship position to the database
                ship_position = ShipPosition.objects.create(row=row, column=column)
                return JsonResponse({'status': 'success', 'id': ship_position.id})
            else:
                return JsonResponse({'status': 'fail', 'error': 'Row and column are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'error': 'Invalid JSON format.'}, status=400)
    
    return JsonResponse({'status': 'fail', 'error': 'Invalid request method.'}, status=405)
def save_board(request):
    if request.method == 'POST':
        board_data = request.POST.get('boardData')
        try:
            board_array = json.loads(board_data) 

            # Get the Game instance 
            game_id = request.session.get('game_id')
            game = get_object_or_404(Game, id=game_id)

            # Reshape the 1D array into a 10x10 2D array
            board_2d = [board_array[i:i+10] for i in range(0, len(board_array), 10)]

            # Extract ship positions from the 2D board_array
            ship_positions = []
            for row_index, row in enumerate(board_2d):
                for col_index, cell_value in enumerate(row):
                    if cell_value == 1: 
                        ship_positions.append({'row': row_index, 'column': col_index})

            # Update the ship_positions field in the Game instance
            game.ship_positions = ship_positions
            game.save()

            return HttpResponse("Board saved successfully!<br>Your id is "+str(game_id))

        except json.JSONDecodeError:
            return HttpResponse("Invalid board data", status=400)
    else:
        return HttpResponse("Invalid request method")