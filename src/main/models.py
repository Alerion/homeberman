# -*- coding: utf-8 -*-

from django.db import models
from accounts.models import User
class Game(models.Model):
    name = models.CharField(max_length=140, null=True, blank=True)
    is_waiting = models.BooleanField(u"Waiting users", default=True)

    players = models.ManyToManyField(User, blank=True)
    
