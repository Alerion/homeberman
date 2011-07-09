from utils.decorators import render_to
from django.conf import settings
from django.shortcuts import get_object_or_404
from models import Game


@render_to('main/index.html')
def index(request):
    return {
        'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
        'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
    }

@render_to('main/list.html')
def list(request):
    games = Game.objects.filter(status=DS_WAITING)
    user = request.user
    return locals()

def join(request, id)
    game = get_object_or_404(Game, id=id)
    if game.status != GS_WAITING and
       game.max_players >= game.players.all().count():
        return HTTPResponceRedirect(reverse('list'))

