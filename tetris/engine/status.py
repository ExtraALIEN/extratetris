active_rooms = {}  #  {room_id: Room instance}
room_lobby = {}    #  {room_id: set() websockets entered room}
in_room_lobby = {} # {conn : room_id }
connections = {}   # {websocket:  {room_id: x, pos: x}   }  (fast find room where connected)
players = {}   # {player:  {room_id: x, pos: x}   }  (fast find room where connected)
ready = {} # {room_id: set() websockets entered room}
room_bots = {} # {room_id : set() positions where is bot}

total_lobby = set()

def all_ready(id):
    room = active_rooms[id]
    return len(ready[id]) == room.human_players()
