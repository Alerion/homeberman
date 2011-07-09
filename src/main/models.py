# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from django.db import models
from accounts.models import User

GS_WAITING = 0
GS_PLAYING = 1
GS_FINISHED = 2

GAME_STATUS_CHOICES = (
    (GS_WAITING, _("Waiting for players")),
    (GS_PLAYING, _("Playing")),
    (GS_FINISHED, _("Finished")),
)

GAME_SIZE_CHOICES = (
    ("small", _(u"Small")),
    ("medium", _(u"Medium")),
    ("big", _(u"Big")),
)

class Player(models.Model):
    user = models.ForeignKey(User)
    cell = models.ForeignKey('Cell')
    game = models.ForeignKey('Game')
    is_dead = models.BooleanField(default=False)
    last_move_time = models.BigIntegerField(default=0)


class Game(models.Model):
    name = models.CharField(max_length=140, null=True, blank=True)
    status = models.IntegerField(default=0, choices=GAME_STATUS_CHOICES)
    max_players = models.PositiveIntegerField(default=10)
    size = models.CharField(default='small', choices=GAME_SIZE_CHOICES, max_length=10)
    winner = models.ForeignKey(Player, related_name='winned_games', null=True)


class Cell(models.Model):
    game = models.ForeignKey(Game, related_name='cells')
    x = models.IntegerField()
    y = models.IntegerField()
    type = models.IntegerField(default=0)
    class Meta:
        unique_together = (('game', 'x', 'y'),)
