from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from accounts.views import create

urlpatterns = patterns('',
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^create/$', create, name='create'),
)
