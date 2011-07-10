from utils.decorators import render_to
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import random

from main.models import Game, Cell, Player, CT_EMPTY, CT_WALL
from accounts.models import User
from forms import GameForm


@render_to('main/index.html')
def index(request):
    game = request.user.get_current_game()
    if not game:
        return redirect('main:list_games')
    
    #generate(game,request.user)
    
    return {
        'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
        'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
    }

@render_to('main/add_game.html')
def add_game(request):
    user = request.user
    old_game = user.get_current_game()
    
    if old_game:
        redirect('main:index')
        
    print request.POST
    form = GameForm(request.POST or None)

    print form.errors
    print form.is_valid()
    if form.is_valid():
        game = form.save()
        player = Player(user=user, game=game)
        player.save()
        return redirect('main:index')

    return dict(form=form)


@render_to('main/game_list.html')
def list_games(request):
    games = Game.are_waiting.all()
    playing = Game.are_playing.all()
    return locals()

def join_game(request, id):
    user = request.user
    old_game = user.get_current_game()
    
    if old_game:
        redirect('main:index')
        
    game = get_object_or_404(Game.are_waiting, id=id)
    
    if game.players.all().count() >= game.max_players:
        redirect('main:list_games')

    player = Player(user=user, game=game)
    player.save()
    return redirect('main:index')


def generate(game, user):
    width = 30
    height = 20
    
    for x in range(width):
        for y in range(height):
            cell = Cell(game=game)
            if random.random() < 0.2 and x not in (0, width-1) and y not in (0, height-1):
                cell.type = CT_WALL
            else:
                cell.type = CT_EMPTY

            cell.x = x
            cell.y = y
            cell.save()
    
    player = Player(user=user, game=game)
    player.cell = Cell.objects.get(x=0, y=0, game=game)
    player.save()
    
    user1 = User.objects.get(pk=2)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=width-1, y=0, game=game)
    player.save()
    
    user1 = User.objects.get(pk=3)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=0, y=height-1, game=game)
    player.save()
        
    user1 = User.objects.get(pk=4)
    player = Player(user=user1, game=game)
    player.cell = Cell.objects.get(x=width-1, y=height-1, game=game)
    player.save()            
