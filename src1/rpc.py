from main.rpc import GameApiClass
from tornado_rpc import RpcRouter

class CustomRouter(RpcRouter):
    
    def __init__(self):
        super(CustomRouter, self).__init__('/rpc/')
        self.host = 'http://127.0.0.1:8000'        
        self.actions = {
            'GameApi': GameApiClass()
        }
        self.enable_buffer = 100
        self.max_retries = 1
        
    def extra_kwargs(self, handler, *args, **kwargs):
        output = super(CustomRouter, self).extra_kwargs(handler, *args, **kwargs)
        output['game'] = handler.user.get_current_game()
        output['player'] = handler.user.get_player()
        return output
        
rpc_router = CustomRouter()

