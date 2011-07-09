# -*- coding: utf-8 -*-

import os, sys, site
from os.path import join

PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

def rel(*x):
    return os.path.join(PROJECT_ROOT, *x)
    
sys.stdout = sys.stderr
sys.path.insert(0, rel('src'))
site.addsitedir(rel('env/lib/python2.6/site-packages'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()