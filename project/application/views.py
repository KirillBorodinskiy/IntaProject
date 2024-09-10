from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Game
from .forms import GameCreationForm
from django.http import JsonResponse
import json


# Create your views here.
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
            return redirect('create-board.html', game_id=game.id)  # Перенаправление на страницу с деталями игры
    else:
        form = GameCreationForm()
    return render(request, 'create-game.html', {'form': form})

def create_board(request):
    # Create an empty 10x10 board as a dictionary
    board = {row_index: {col_index: '' for col_index in range(10)} for row_index in range(10)}

    ShipList = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    return render(request, 'create-board.html', {'board': board, 'ShipList': ShipList})

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

def place_ship(request):
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        orientation = request.POST.get('orientation')



        # Возвращаем ответ (можно перенаправить на ту же страницу или другую)
        updated_board = 1

        return render(request, 'create-board.html', {'board': updated_board})  # Или другую страницу, если нужно

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
