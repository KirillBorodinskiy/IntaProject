from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
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
                player_1=player_1_board.player, 
                player_2=player_2_board.player,
                current_turn=player_1_board.player,  
                player_1_board=player_1_board,
                player_2_board=player_2_board
            )

            player_1_board.in_game = True 
            player_1_board.save()
            player_2_board.in_game = True
            player_2_board.save()

            return redirect('game_view', game_id=game.id) 
    else:
        form = ConnectTablesForm()

    return render(request, 'connect-tables.html', {'form': form})

def board_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Get the boards for both players
    player_1_board = game.player_1_board
    player_2_board = game.player_2_board

    # Access ship positions directly from the TextField, converting to a list if needed
    board_1_data = eval(player_1_board.ship_positions) if player_1_board.ship_positions else []
    board_2_data = eval(player_2_board.ship_positions) if player_2_board.ship_positions else []

    # Construct the board dictionaries in the desired format
    board_1 = {row_index: {col_index: cell_value for col_index, cell_value in enumerate(row)} 
                for row_index, row in enumerate(board_1_data)}
    board_2 = {row_index: {col_index: cell_value for col_index, cell_value in enumerate(row)} 
                for row_index, row in enumerate(board_2_data)}

    # Pass the boards to the template
    return render(request, 'board.html', {'boards': {'player_1': board_1, 'player_2': board_2}})

def index(request):
    return HttpResponse("haha")

def create_board(request):
    # Associate the board with the current user
    player = request.user 

    # Create a new Board instance with an empty ship_positions list
    board = Board.objects.create(player=player)

    # Create an empty 10x10 board as a dictionary
    LocalBoard = {row_index: {col_index: '' for col_index in range(10)} for row_index in range(10)}
    ShipList = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] 

    # Store the board_id in the session 
    request.session['board_id'] = board.id

    return render(request, 'create-board.html', {'board': LocalBoard, 'ShipList': ShipList})

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
        
        # Get the Board instance 
        board_id = request.session.get('board_id')
        board = get_object_or_404(Board, id=board_id)

        # Update the ship_positions field in the Board instance
        board.ship_positions = board_data
        board.save()

        return render(request, 'save-board.html')
    else:
        return HttpResponse("Invalid request method")