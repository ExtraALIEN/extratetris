active_rooms = {}  #  {room_id: Room instance}
room_lobby = {}    #  {room_id: set() websockets entered room}
in_room_lobby = {} # {conn : room_id }
connections = {}   # {websocket:  {room_id: x, pos: x}   }  (fast find room where connected)
players = {}   # {player:  {room_id: x, pos: x}   }  (fast find room where connected)
