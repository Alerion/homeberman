from utils.decorators import render_to
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from main.models import MOVE_TIME, EXPLOSION_TIME
from accounts.models import User
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
        'game': game,
        'MOVE_TIME': MOVE_TIME,
        'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
        'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
    }

@render_to('main/games_history.html')
def games_history(request):
    
    return {
        'games': Game.are_finished.filter(players__user=request.user)
    }

@render_to('main/finished.html')
def finished(request, game_id):
    game = get_object_or_404(Game.objects.select_related('players', 'players__user'), pk=game_id)
    return {
        'game': game
    }

@render_to('main/add_game.html')
def add_game(request):
    user = request.user
    old_game = user.get_current_game()
    
    if old_game:
        return redirect('main:index')
        
    form = GameForm(request.POST or None)

    if form.is_valid():
        game = form.save()
        game.generate_map()
        game.add_user(request.user)
        return redirect('main:index')

    return dict(form=form)

@render_to('main/game_list.html')
def list_games(request):
    cur_game = request.user.get_current_game()

    if cur_game:
        return redirect('main:index')
        
    games = Game.are_waiting.select_related('playeres', 'players__user')
    playing = Game.are_playing.all()
    return locals()

def join_game(request, id):
    user = request.user
    old_game = user.get_current_game()
    
    if old_game:
        return redirect('main:index')
    
    if user.in_game():
        return redirect('main:list_games')
        
    game = get_object_or_404(Game.are_waiting, id=id)
    
    if game.players.all().count() >= game.max_players:
        return redirect('main:list_games')
        
    game.add_user(user)

    return redirect('main:list_games')     
