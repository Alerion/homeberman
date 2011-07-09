from utils.decorators import render_to
from django.conf import settings

@render_to('main/index.html')
def index(request):
    return {
        'ORBITED_STOMP_SOCKET': settings.ORBITED_STOMP_SOCKET,
        'ORBITED_HTTP_SOCKET': settings.ORBITED_HTTP_SOCKET
    }