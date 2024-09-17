from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from .forms import ConnectTablesForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

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
                player_2_board=player_2_board,
                updated_at=datetime.now()
            )

            player_1_board.in_game = True 
            player_1_board.save()
            player_2_board.in_game = True
            player_2_board.save()

            return redirect('game_view', game_id=game.id) 
    else:
        form = ConnectTablesForm()

    return render(request, 'connect-tables.html', {'form': form})

@login_required
def board_view(request, game_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    r = range(11)
    n = [0,1,2,3,4,5,6,7,8,9,10]
    l = ['Z','A','B','C','D','E','F','G','H','I','J']
    rn = list(zip(r, n))
    rl = list(zip(r, l))

    game = get_object_or_404(Game, id=game_id)

    # Get the boards for both players
    player_1_board = game.player_1_board
    player_2_board = game.player_2_board

    player_1 = game.player_1
    player_2 = game.player_2

    if 'last_update_time' not in request.session:
        request.session['last_update_time'] = game.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    # Access ship positions directly from the TextField, converting to a list if needed
    board_1_data = eval(player_1_board.ship_positions) if player_1_board.ship_positions else []
    board_2_data = eval(player_2_board.ship_positions) if player_2_board.ship_positions else []

    winner = game.winner

    # Construct the board dictionaries in the desired format
    board_1 = {row_index: {col_index: cell_value for col_index, cell_value in enumerate(row)} 
                for row_index, row in enumerate(board_1_data)}
    board_2 = {row_index: {col_index: cell_value for col_index, cell_value in enumerate(row)} 
                for row_index, row in enumerate(board_2_data)}

    # Pass the boards to the template
    return render(request, 'board.html', {'boards': {player_1: board_1, player_2: board_2}, 'rn': rn, 'rl': rl,'game_id':game_id, 'current_turn': game.current_turn.username,'winner':winner})

def start_page(request):
    return render(request, 'start-page.html')

def create_board(request):
    r = range(11)
    n = [0,1,2,3,4,5,6,7,8,9,10]
    l = ['Z','A','B','C','D','E','F','G','H','I','J']
    rn = list(zip(r, n))
    rl = list(zip(r, l))

    # Associate the board with the current user
    player = request.user 



    # Create an empty 10x10 board as a dictionary
    LocalBoard = {row_index: {col_index: '' for col_index in range(10)} for row_index in range(10)}
    ShipList = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] 

    return render(request, 'create-board.html', {'board': LocalBoard, 'ShipList': ShipList, 'rn': rn, 'rl': rl})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def update_board(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            row = data.get('row')
            column = data.get('col')
            game_id = data.get('game_id')

            if row is not None and column is not None and game_id is not None:
                try:
                    game = Game.objects.get(id=game_id)
                except Game.DoesNotExist:
                    return JsonResponse({'status': 'fail', 'error': 'Game not found.'}, status=400)
                if(game.winner!=None):
                    return JsonResponse({'status': 'fail', 'error': 'Winner was found.'+str(game.winner)}, status=200)
                # Determine the opponent's board
                opponent_board = None
                if game.current_turn == request.user:
                    if (request.user==game.player_1):
                        opponent_board=game.player_2_board
                    else:
                        opponent_board=game.player_1_board

                if opponent_board is None:
                    return JsonResponse({'status': 'fail', 'error': 'Not your turn.'}, status=400)
                # Update the cell in the opponent's board data
                opponent_board_data = eval(opponent_board.ship_positions)
                if 0 <= row < 10 and 0 <= column < 10:  # Check if row and column are within bounds
                    if opponent_board_data[row][column] == '1':
                        opponent_board_data[row][column] = '2'  # Hit
                        
                    elif(opponent_board_data[row][column] == '0'):
                        opponent_board_data[row][column] = '3'  # Miss
                        if (request.user==game.player_1):
                            game.current_turn=game.player_2
                        else:
                            game.current_turn=game.player_1
                        game.updated_at=datetime.now()
                        
                    # Checking the board to decide if we have a winner
                    flattened_board = [cell for row in opponent_board_data for cell in row]

                    if(flattened_board.count("1")==0):
                        game.winner=request.user
                    game.save()

                    # Save the updated board data back to the Board instance
                    opponent_board.ship_positions = repr(opponent_board_data)
                    opponent_board.save()

                    return JsonResponse({'status': 'success', 'hit at': str(row)+' '+str(column)})
                else:
                    return JsonResponse({'status': 'fail', 'error': 'Invalid row or column.'}, status=400)

            else:
                return JsonResponse({'status': 'fail', 'error': ''+str(row)+', '+str(column)+', and '+str(game_id)+' are required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'error': 'Invalid JSON format.'}, status=400)

    return JsonResponse({'status': 'fail', 'error': 'Invalid request method.'}, status=405)

def check_for_updates(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Check if it's the current user's turn
    if game.current_turn == request.user:
        return JsonResponse({'update': False})

    last_update_time_str = request.session.get('last_update_time')
    if last_update_time_str is None:
        last_update_time = game.updated_at
    else:
        last_update_time = timezone.make_aware(datetime.strptime(last_update_time_str, '%Y-%m-%d %H:%M:%S')) 

    # Check if the game has been updated since the last check
    if game.updated_at > last_update_time: 
        request.session['last_update_time'] = game.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse({'update': True})
    else:
        return JsonResponse({'update': False})

def save_board(request):
    if request.method == 'POST':
        board_data = request.POST.get('boardData')
        
        # Get the Board instance 
        board = Board.objects.create(player=request.user)

        # Update the ship_positions field in the Board instance
        board.ship_positions = board_data
        board.save()

        return render(request, 'save-board.html', {'board': board})
    else:
        return HttpResponse("Invalid request method")

@login_required
def games_view(request):
    # Get the logged-in user
    user = request.user

    # Query games where the user is either player_1 or player_2
    games_as_player_1 = Game.objects.filter(player_1=user)
    games_as_player_2 = Game.objects.filter(player_2=user)

    # Combine both queries into a single list of games
    games = games_as_player_1 | games_as_player_2

    # Pass the games to the template
    return render(request, 'games_list.html', {'games': games})