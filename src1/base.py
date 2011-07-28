import tornado.web
from django.utils.importlib import import_module
from accounts.models import User
from tornado.escape import xhtml_escape
from django.utils.safestring import SafeData
from django.utils.datastructures import MultiValueDict

def save_escape(value):
    if isinstance(value, SafeData):
        return value
    return xhtml_escape(value)

class BaseHandler(tornado.web.RequestHandler):
    
    user = tornado.web.RequestHandler.current_user
    
    def request_data(self):
        return MultiValueDict(self.request.arguments)
    
    def render(self, template_name, **kwargs):
        if not 'url' in kwargs:
            kwargs['url'] = self.reverse_url
        
        if not 'user' in kwargs:
            kwargs['user'] = self.user
        
        if not 'static' in kwargs:
            kwargs['static'] = self.static_url
        
        kwargs['save_escape'] = save_escape
        
        return super(BaseHandler, self).render(template_name, **kwargs)
    
    def get_current_user(self):
        session_key = self.settings['auth_session_key']
        user_id = self.session.get(session_key)
        
        if not user_id:
            return
        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
    
    def prepare(self):
        print 'PREPARE'
        cookie_name = self.settings['session_cookie_name']
        engine = import_module(self.settings['session_engine'])
        session_key = self.get_secure_cookie(cookie_name)
        self.session = engine.SessionStore(session_key)
    
    def post_request(self):
        try:
            modified = self.session.modified
        except AttributeError:
            pass
        else:
            if modified:
                self.session.save()
                cookie_name = self.settings['session_cookie_name']
                self.set_secure_cookie(cookie_name, self.session.session_key)
        print 'FINISH'
    
    def finish(self, *args, **kwargs):
        self.post_request()
        super(BaseHandler, self).finish(*args, **kwargs)
        
class GoogleHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, data):
        if not data:
            raise tornado.web.HTTPError(500, "Google auth failed")
        
        try:
            user = User.objects.get(username=data['email'])
        except User.DoesNotExist:
            user = User()
            user.email = data['email']
            user.username = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.set_unusable_password()
            user.save()
            
        session_key = self.settings['auth_session_key']
        self.session[session_key] = user.pk
        self.redirect('/')
