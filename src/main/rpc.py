from utils.rpc import Error, Msg, RpcExceptionEvent, add_request_to_kwargs
from utils.rpc import RpcRouter
from utils.stomp_utils import stomp_send

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
    
    def func1(self, user):
        return {}
        
router = RpcRouter('main:router', {
    'MainApi': MainApiClass(),
    'GameApi': GameApiClass()
})