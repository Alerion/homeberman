from django.core.management.base import BaseCommand
from main.models import Cell, EXPLOSION_TIME
import time

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        while 1:
            put_time = time.time() - EXPLOSION_TIME
            
            qs = Cell.objects.filter(bomb_time__lte=put_time).order_by('bomb_time') \
                .select_related('game')
            for cell in qs:
                cell.explode()
                
            time.sleep(0.5)