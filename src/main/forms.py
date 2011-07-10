# -*- coding: utf-8 -*-
from django import forms
from models import Game

class GameForm(forms.ModelForm):
    max_players = forms.IntegerField(max_value=8, min_value=1, initial=4,
                help_text=u'1-8 игроков', label=u'Кол. игроков')
    death_limit = forms.IntegerField(max_value=20, min_value=1, initial=3,
                help_text=u'1-20', label=u'лимит смертей')
    unmove_max_time = forms.IntegerField(max_value=30, min_value=5, initial=10,
                help_text=u'5-30 сек.', label=u'макс. AFK')
    
    class Meta:
        fields = ['name', 'max_players', 'size', 'death_limit', 'unmove_max_time']
        model = Game

        

