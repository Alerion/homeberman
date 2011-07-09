from utils.rpc import Error, Msg, RpcExceptionEvent, add_request_to_kwargs
from utils.rpc import RpcRouter
from utils.stomp_utils import stomp_send
from main.models import CT_EMPTY, CT_WALL
import random
    
class GameApiClass(object):
    width = 30
    height = 20
    
    def put_bomb(self, x, y, user, game):
        return True
    
    def move(self, x, y, user, game):
        return True
    
    def load_players(self, user, game):
        return {
            'player': {
                'name': unicode(user),
                'x': 0,
                'y': 0                
            },
            'enemies': [{
                'name': 'Player 1',
                'x': self.width-1,
                'y': 0,
                'id': 1000
            },{
                'name': 'Player 2',
                'x': 0,
                'y': self.height-1,
                'id': 10001
            },{
                'name': 'Player 3',
                'x': self.width-1,
                'y': self.height-1,
                'id': 10002
            }]
        }
    
    def load_map(self, user, game):
        output = {}
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if random.random() < 0.2:
                    output['%s_%s' % (x, y)] = CT_WALL
                else:
                    output['%s_%s' % (x, y)] = CT_EMPTY
        return {
            'cells': output,
            'width': 30,
            'height': 20
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
        return output
        
router = CustomRouter()