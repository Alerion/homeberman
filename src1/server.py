#!/usr/bin/env python

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import os
import sys

#add base project to Python PATH and Django settings
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)
sys.path.insert(0, rel('src'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self, **kwargs):
        
        handlers = [
            (r"/", MainHandler),
        ]    
        settings = dict()
        kwargs.update(settings)
        tornado.web.Application.__init__(self, handlers, **kwargs)

class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write("Hello, world")
        
def main():
    tornado.options.parse_command_line()
    app = Application(debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(num_processes=1)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()