from django.core.management.base import BaseCommand
from main.models import Cell, Player, EXPLOSION_TIME, RESPOWN_TIME, GS_PLAYING
import time
from django.db.models import F

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        while 1:
            #explode bomb
            put_time = time.time() - EXPLOSION_TIME
            
            qs = Cell.objects.filter(bomb_time__lte=put_time).order_by('bomb_time') \
                .select_related('game')
            
            for cell in qs:
                cell.explode()
            
            #respown players
            death_time = time.time() - RESPOWN_TIME
            
            qs = Player.objects.exclude(death_time=0).filter(death_time__lte=death_time) \
                .filter(game__status=GS_PLAYING) \
                .order_by('death_time').select_related('game')
            
            for player in qs:
                player.respown()
            
            #check unmove time
            qs = Player.objects.exclude(last_move_time=0) \
                .filter(is_dead=False) \
                .filter(last_move_time__lte=time.time()-F('game__unmove_max_time')) \
                .filter(game__status=GS_PLAYING) \
                .order_by('last_move_time').select_related('game')
            
            for player in qs:
                player.kill()
            
            time.sleep(0.5)