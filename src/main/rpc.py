from utils.rpc import Error, Msg, RpcExceptionEvent, add_request_to_kwargs
from utils.rpc import RpcRouter
from utils.stomp_utils import stomp_send
from main.models import CT_EMPTY, CT_WALL
import random
    
class GameApiClass(object):
    width = 30
    height = 20
    
    def put_bomb(self, x, y, user, player, game):
        return True
    
    def move(self, x, y, user, player, game):
        return player.move_to(x, y)
    
    def load_players(self, user, player, game):
        enemies = []
        for p in game.player_set.exclude(pk=player.pk):
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
        self.url = 'main:router'
        self.actions = {
            'GameApi': GameApiClass()
        }
        self.enable_buffer = 50
        self.max_retries = 1
    
    def extra_kwargs(self, request, *args, **kwargs):
        output = super(CustomRouter, self).extra_kwargs(request, *args, **kwargs)
        output['game'] = request.user.get_current_game()
        output['player'] = request.user.get_player()
        return output
        
router = CustomRouter()