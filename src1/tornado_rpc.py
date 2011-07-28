import utils.rpc as rpc
import tornado.web
from django.utils import simplejson
import urllib
from base import BaseHandler
from utils.rpc import RpcMultiValueDict, RpcExceptionEvent
from inspect import getargspec

#Does not support URL args for Router

class RpcRequestHandler(BaseHandler):
    
    def initialize(self, rpc):
        self.rpc = rpc
    
    def get(self, *args, **kwargs):
        self.write(self.rpc.js_initialization(args, kwargs))
    
    def post(self):
        self.rpc(self)
        self.finish()
    
class TornadoRpcRouterJSONEncoder(rpc.RpcRouterJSONEncoder):
    
    def __init__(self, *args, **kwargs):
        super(TornadoRpcRouterJSONEncoder, self).__init__(*args, **kwargs)
        self.router_classes = (RpcRouter,)
    
    def _get_url(self, obj):
        #FIXME: should apply args and kwargs from URL
        #args=self.url_args, kwargs=self.url_kwargs
        return obj.host+obj.url

class RpcRouter(object):
    """
    Router for jQuery.Rpc calls.
    """    
    def __init__(self, url, actions={}, enable_buffer=True, max_retries=0):
        #FIXME: url should be url name
        self.url = url
        self.actions = actions
        self.enable_buffer = enable_buffer
        self.max_retries = max_retries

    def url_pattern(self):
        #FIXME: url should be url name
        return tornado.web.url(self.url, RpcRequestHandler, {'rpc': self}, 'rpc')
        
    def __call__(self, handler, *args, **kwargs):
        """
        This method is view that receive requests from Ext.Direct.
        """
        request = handler.request
        
        try:
            requests = simplejson.loads(urllib.unquote_plus(request.body))
        except (ValueError, KeyError, IndexError):
            requests = []
            
        if not isinstance(requests, list):
                requests = [requests]
            
        output = []
        
        for rd in requests:
            mr = self.call_action(rd, handler, *args, **kwargs)
            
            #This looks like a little ugly
            if 'result' in mr and isinstance(mr['result'], rpc.RpcHttpResponse):
                for key, val in mr['result'].cookies.items():
                    handler.set_cookie(key, val.value, val['domain'], val['expires'], val['path'],
                                        **{'secure': val['secure'], "max-age": val['max-age']})
                mr['result'] = dict(mr['result'])
                
            output.append(mr)
        
        handler.write(simplejson.dumps(output))
            
        return handler

    def call_action(self, rd, handler, *args, **kwargs):
        """
        This method checks parameters of Ext.Direct request and call method of action.
        It checks arguments number, method existing, handle RpcExceptionEvent and send
        exception event for Ext.Direct.
        """        
        method = rd['method']

        if not rd['action'] in self.actions:
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': 'Undefined action'
            }
        
        action = self.actions[rd['action']]
        
        if not hasattr(action, method):
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': 'Undefined method'
            }
                    
        func = getattr(action, method)
        
        args = []
        for val in (rd.get('data') or []):
            if isinstance(val, dict):
                val = RpcMultiValueDict(val)
            args.append(val)

        extra_kwargs = self.extra_kwargs(handler, *args, **kwargs)
        extra_kwargs.update(self.action_extra_kwargs(action, handler, *args, **kwargs))
        extra_kwargs.update(self.method_extra_kwargs(func, handler, *args, **kwargs))
        
        func_args, varargs, varkw, func_defaults = getargspec(func)
        func_args.remove('self') #TODO: or cls for classmethod
        for name in extra_kwargs.keys():
            if name in func_args:
                func_args.remove(name)
        
        required_args_count = len(func_args) - len(func_defaults or [])
        if (required_args_count - len(args)) > 0 or (not varargs and len(args) > len(func_args)):
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': 'Incorrect arguments number'
            }
        
        try:
            return {
                'tid': rd['tid'],
                'type': 'rpc',
                'action': rd['action'],
                'method': method,
                'result': func(*args, **extra_kwargs)
            }
        except RpcExceptionEvent, e:
            return {
                'tid': rd['tid'],
                'type': 'exception',
                'action': rd['action'],
                'method': method,
                'message': unicode(e)
            }  
    
    def action_extra_kwargs(self, action, handler, *args, **kwargs):
        """
        Check maybe this action get some extra arguments from request
        """  
        if hasattr(action, '_extra_kwargs'):
            return action._extra_kwargs(handler, *args, **kwargs)
        return {}
    
    def method_extra_kwargs(self, method, handler, *args, **kwargs):
        """
        Check maybe this method get some extra arguments from request
        """  
        if hasattr(method, '_extra_kwargs'):
            return method._extra_kwargs(handler, *args, **kwargs)
        return {}
        
    def extra_kwargs(self, handler, *args, **kwargs):
        """
        For all method in ALL actions we add request.user to arguments. 
        You can add something else, request for example.
        For adding extra arguments for one action use action_extra_kwargs.
        """        
        return {
            'user': handler.user
        }

    def js_initialization(self, args, kwargs, encoder=TornadoRpcRouterJSONEncoder):
        obj = simplejson.dumps(self, cls=encoder, url_args=args, url_kwargs=kwargs)
        return 'jQuery.Rpc.addProvider(%s)' % obj