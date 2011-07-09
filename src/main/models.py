# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from django.db import models
from accounts.models import User


GAME_STATUS_CHOICES = (
    (0, _("Waiting for players")),
    (1, _("Playing")),
    (2, _("Finished")),
)

class Player(models.Model):
    user = models.ForeignKey(User)
    cell = models.ForeignKey('Cell')
    game = models.ForeignKey('Game')
    

class Game(models.Model):
    name = models.CharField(max_length=140, null=True, blank=True)
    status = models.IntegerField(default=0, choices=GAME_STATUS_CHOICES)

class Cell(models.Model):
    game = models.ForeignKey(Game, related_name='cells')
    x = models.IntegerField()
    y = models.IntegerField()
    type = models.CharField(max_length=10)
    class Meta:
        unique_together = (('game', 'x', 'y'),)
