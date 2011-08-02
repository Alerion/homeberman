#!/usr/bin/env python

import os
import sys
#add base project to Python PATH and Django settings
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)
sys.path.insert(0, rel('src'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.auth
import tornadio
import tornadio.router
import tornadio.server
from datetime import timedelta, datetime
import time

from main.models import Game, Cell, Player, EXPLOSION_TIME, RESPOWN_TIME, GS_PLAYING, GAME_START_WAITING
from django.db.models import F
from main.forms import GameForm

from rpc import rpc_router
from base import BaseHandler, GoogleHandler
from conn_manager import connection_manager

class Application(tornado.web.Application):
    
    def __init__(self, **kwargs):
        from django.conf import settings

        self.connection_manager = connection_manager

        handlers = [
            tornado.web.url(r"/", MainHandler, name='main'),
            tornado.web.url(r"/login/", GoogleHandler, name='login'),
            tornado.web.url(r"/list/", GameListHandler, name='list_games'),
            tornado.web.url(r"/add/", AddGameHandler, name='add_game'),
            tornado.web.url(r"/finish/", FinishHandler, name='finish'),
            rpc_router.url_pattern(),
            GameSocketRouter.route(),
        ]    
        settings = dict(
            login_url = '/login/',
            cookie_secret = 'asdadasddfasdf',
            session_cookie_name = 'sessionid',
            auth_session_key = '_auth_user_id',
            session_engine = settings.SESSION_ENGINE,
            template_path = 'templates',
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape='save_escape',
            socket_io_port = 8000,
            flash_policy_port = 843,
            flash_policy_file = os.path.join(os.path.dirname(__file__), "static", 'flashpolicy.xml')            
        )
        kwargs.update(settings)
        tornado.web.Application.__init__(self, handlers, **kwargs)

class GameSocketConnection(tornadio.SocketConnection):
    
    def on_open(self, handler, *args, **kwargs):
        self.key = handler.user.get_current_game().stomp_key()
        handler.application.connection_manager.add(self.key, self)

    def on_message(self, message):
        pass
    
    def on_close(self, handler):
        handler.application.connection_manager.remove(self.key, self)

GameSocketRouter = tornadio.get_router(GameSocketConnection, dict(
    enabled_protocols=['websocket', 'flashsocket']
))

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

        context = {
            'games': Game.are_waiting.select_related('playeres', 'players__user'),
            'playing': Game.are_playing.all()
        }
        self.render('main/game_list.html', **context)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print self.application
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

def bomb_monitor():
    put_time = time.time() - EXPLOSION_TIME

    qs = Cell.objects.filter(bomb_time__lte=put_time).order_by('bomb_time') \
        .select_related('game')
    
    for cell in qs:
        cell.explode()
    
    #respown players
    death_time = time.time() - RESPOWN_TIME
    
    qs = Player.objects.exclude(death_time=0).filter(death_time__lte=death_time) \
        .filter(game__status=GS_PLAYING) \
        .order_by('death_time').select_related('game')
    
    for player in qs:
        player.respown()
    
    #check unmove time
    qs = Player.objects.exclude(last_move_time=0) \
        .filter(is_dead=False) \
        .filter(last_move_time__lte=time.time()-F('game__unmove_max_time')) \
        .filter(game__status=GS_PLAYING) \
        .order_by('last_move_time').select_related('game')
    
    for player in qs:
        player.kill()
    
    #start games
    created_date = datetime.now() - timedelta(seconds=GAME_START_WAITING)
    qs = Game.are_waiting.filter(created__lte=created_date)
    
    for game in qs:
        game.start()
                
def main():
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(bomb_monitor, 100, io_loop).start()
    tornadio.server.SocketServer(Application(debug=True), io_loop=io_loop)

if __name__ == "__main__":
    main()