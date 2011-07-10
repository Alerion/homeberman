from django.forms import ModelForm
from models import Game

class GameForm(ModelForm):
    class Meta:
        fields = ['name', 'max_players', 'size']
        model = Game
        
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['max_players'].max_value = 8
        self.fields['max_players'].min_value = 1
        

