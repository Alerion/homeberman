from django.forms import ModelForm
from models import Game

class GameForm(ModelForm):
    class Meta:
        fields = ['name', 'max_players', 'size']
        model = Game

