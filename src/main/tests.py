from django.utils.unittest import TestCase
from models import User, Game, Player, Cell


class TestModels(TestCase):
    def dummyGameModel(self):
        g = Game(name="TestGame")
        g.save()

