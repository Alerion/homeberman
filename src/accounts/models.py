from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.db.models.signals import post_save

class User(BaseUser):
    
    objects = UserManager()
    
    def get_stomp_key(self):
        return self.pk
    
    def get_player(self):
        game = self.get_current_game()
        
        if game:
            return game.players.get(user=self)
    
    def in_game(self):
        from main.models import Game, GS_PLAYING, GS_WAITING
        Q = models.Q
        return Game.objects.filter(players__user=self) \
            .filter(Q(status=GS_PLAYING)|Q(status=GS_WAITING)).exists()
    
    def get_current_game(self):
        from main.models import Game, GS_PLAYING
        try:
            return Game.are_playing.filter(players__user=self)[:1].get()
        except Game.DoesNotExist:
            pass
    
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = User(**values)
        user.save()
        
post_save.connect(create_custom_user, BaseUser)
