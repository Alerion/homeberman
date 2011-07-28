#!/usr/bin/env python

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.auth
from tornado.options import define, options
import simplejson as json
import os
import sys

#add base project to Python PATH and Django settings
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)
sys.path.insert(0, rel('src'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

define("port", default=8000, help="run on the given port", type=int)

from main.models import Game
from main.forms import GameForm

from rpc import rpc_router
from base import BaseHandler, GoogleHandler

class Application(tornado.web.Application):

    def __init__(self, **kwargs):
        from django.conf import settings
        
        
        handlers = [
            tornado.web.url(r"/", MainHandler, name='main'),
            tornado.web.url(r"/login/", GoogleHandler, name='login'),
            tornado.web.url(r"/list/", GameListHandler, name='list_games'),
            tornado.web.url(r"/add/", AddGameHandler, name='add_game'),
            tornado.web.url(r"/finish/", FinishHandler, name='finish'),
            rpc_router.url_pattern(),
        ]    
        settings = dict(
            login_url = '/login/',
            cookie_secret = 'asdadasddfasdf',
            session_cookie_name = 'sessionid',
            auth_session_key = '_auth_user_id',
            session_engine = settings.SESSION_ENGINE,
            template_path = 'templates',
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape='save_escape'
        )
        kwargs.update(settings)
        tornado.web.Application.__init__(self, handlers, **kwargs)

class FinishHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        self.write('FINISH')

class AddGameHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        user = self.user
        old_game = user.get_current_game()
        
        if old_game:
            return self.redirect(self.reverse_url('main'))
        
        form = GameForm()
            
        context = dict(
            form = form
        )
        self.render('main/add_game.html', **context)
    
    @tornado.web.authenticated
    def post(self):
        form = GameForm(self.request_data())
    
        if form.is_valid():
            game = form.save()
            game.generate_map()
            game.add_user(self.user)
            return self.redirect(self.reverse_url('main'))

        context = dict(
            form = form
        )
        self.render('main/add_game.html', **context)
    
class GameListHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        cur_game = self.user.get_current_game()

        if cur_game:
            return self.redirect(self.reverse_url('main'))
        
        context = dict(
            games = Game.are_waiting.select_related('playeres', 'players__user'),
            playing = Game.are_playing.all()
        )
        self.render('main/game_list.html', **context)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        from django.conf import settings
        from main.models import MOVE_TIME
        
        game = self.user.get_current_game()
        if not game:
            return self.redirect(self.reverse_url('list_games'))
        
        context = {
            'game': game,
            'MOVE_TIME': MOVE_TIME,
            'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
            'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
        }        
        self.render('main/index.html', **context)
        
def main():
    tornado.options.parse_command_line()
    app = Application(debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(num_processes=1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()