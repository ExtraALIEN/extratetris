active_rooms = {}  #  {room_id: Room instance}
room_lobby = {}    #  {room_id: set() websockets entered room}
connections = {}   # {websocket:  room_id   }  (fast find room where connected)
