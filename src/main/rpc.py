from utils.rpc import Error, Msg, RpcExceptionEvent, add_request_to_kwargs
from utils.rpc import RpcRouter

class MainApiClass(object):
    
    def hello(self, val, user):
        print val
        return {
            'msg': u'Hello World %s!' % val,
            'val': val
        }

class GameApiClass(object):
    
    def func1(self, user):
        print user
        return {}
        
router = RpcRouter('main:router', {
    'MainApi': MainApiClass(),
    'GameApi': GameApiClass()
})