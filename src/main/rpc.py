from utils.rpc import Error, Msg, RpcExceptionEvent, add_request_to_kwargs
from utils.rpc import RpcRouter
from utils.stomp_utils import stomp_send
import random

EMPTY = 0
WALL = 1

class MainApiClass(object):
    
    def hello(self, val, user):
        return {
            'msg': u'Hello World %s!' % val,
            'val': val
        }
    
    def test_stomp(self, val, user):
        print 'test stomp'
        data = {
            'msg': u'Hello World %s!' % val,
            'val': val
        }
        stomp_send(data, '/user/%s' % user.get_stomp_key())
    
class GameApiClass(object):
    width = 30
    height = 20
    
    def move(self, x, y, user):
        pass
    
    def load_players(self, user):
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
    
    def load_map(self, user):
        output = {}
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                if random.random() < 0.2:
                    output['%s_%s' % (x, y)] = WALL
                else:
                    output['%s_%s' % (x, y)] = EMPTY
        return {
            'cells': output,
            'width': 30,
            'height': 20
        }
        
router = RpcRouter('main:router', {
    'MainApi': MainApiClass(),
    'GameApi': GameApiClass()
})