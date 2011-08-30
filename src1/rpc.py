from main.rpc import GameApiClass
from tornado_rpc import RpcRouter, SocketRpcRouterBase
from main.models import EXPLOSION_TIME
from django.template.loader import render_to_string
import tornadio

class GameApiClass(object):
    width = 30
    height = 20
    
    def load_panel(self, user, player, game):
        return render_to_string('main/_panel.html', {
            'game': game, 
            'EXPLOSION_TIME': EXPLOSION_TIME
        })
    
    def put_bomb(self, x, y, user, player, game):
        return player.put_bomb()
    
    def move(self, x, y, user, player, game):
        return player.move_to(x, y)
    
    def load_players(self, user, player, game):
        enemies = []
        for p in game.players.exclude(pk=player.pk):
            enemies.append(p.record())
        
        return {
            'player': player.record(),
            'enemies': enemies
        }
    
    def load_map(self, user, player, game):
        output = {}
        qs = game.cells.all()
        
        for cell in qs:
            output[cell.key()] = cell.record()
            
        w, h = game.get_size()

        return {
            'cells': output,
            'width': w,
            'height': h
        }

class CustomRouter(RpcRouter):
    
    def __init__(self):
        super(CustomRouter, self).__init__('/rpc/')
        self.rpc_type = 'socket'
        self.host = 'http://127.0.0.1:8000'        
        self.actions = {
            'GameApi': GameApiClass()
        }
        self.enable_buffer = False
        self.max_retries = 1
        
    def extra_kwargs(self, handler, *args, **kwargs):
        output = super(CustomRouter, self).extra_kwargs(handler, *args, **kwargs)
        output['game'] = handler.user.get_current_game()
        output['player'] = handler.user.get_player()
        return output
        
rpc_router = CustomRouter()