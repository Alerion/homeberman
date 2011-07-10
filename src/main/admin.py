from django.contrib import admin
from main.models import Game, Player, Cell

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_dead')

admin.site.register(Game)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Cell)