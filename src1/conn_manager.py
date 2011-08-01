class ConnectionManager(object):
    
    def __init__(self):
        self._connections = {}       
    
    def add(self, key, connection):
        if not key in self._connections:
            self._connections[key] = set()
        
        self._connections[key].add(connection)

    def remove(self, key, connection=None):
        if key in self._connections:
            if connection:
                self._connections[key].discard(connection)
                if len(self._connections[key]) == 0:
                    del self._connections[key]
            else:
                del self._connections[key]
    
    def get(self, key):
        return self._connections.get(key, set())
    
connection_manager = ConnectionManager()

def send_game_event(data, game):
    key = game.stomp_key()
    for conn in connection_manager.get(key):
        conn.send(data)