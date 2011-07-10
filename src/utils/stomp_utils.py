import stomp
from django.conf import settings
from stomp.exception import ConnectionClosedException, NotConnectedException
from time import sleep
from django.utils import simplejson as json

class StompConnection(stomp.Connection):
    
    def __init__(self, host_and_ports=None, *args, **kwargs):
        host_and_ports = [('localhost', settings.ORBITED_STOMP_SOCKET)]
        super(StompConnection, self).__init__(host_and_ports, *args, **kwargs)
        
stomp_connection = StompConnection()        

def stomp_send(data, destination):
    stomp_connection.start()
    try:
        stomp_connection.connect()
    except (ConnectionClosedException, NotConnectedException):
        sleep(0.5)
        stomp_connection.connect()
    stomp_connection.send(json.dumps(data), destination=destination)
    
def send_user(data, game):
    dest = '/user/%s' % game.stomp_key()
    try:
        stomp_send(data, dest)
    except (ConnectionClosedException, NotConnectedException):
        print 'STOMP ERROR'
        pass