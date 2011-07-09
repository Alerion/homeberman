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
    
    def load_map(self, user):
        output = {}
        width = 30
        height = 20
        for x in range(width):
            for y in range(height):
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