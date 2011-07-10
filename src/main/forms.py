from django import forms
from models import Game

class GameForm(forms.ModelForm):
    max_players = forms.IntegerField(max_value=8, min_value=1)
    
    class Meta:
        fields = ['name', 'max_players', 'size']
        model = Game

        

