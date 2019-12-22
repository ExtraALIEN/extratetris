import engine.status as status

def init_fields(id):
    from engine.roomUtils import broadcast_room
    room = status.active_rooms[id]
    for x in range(len(room.fields)):
        field = room.fields[x]
        print(id, status.room_lobby[id])
        msg = {'type': 'surface',
               'pos' : x,
               'x': 0,
               'y': 0,
               'width' : len(field.surface[0]),
               'height': len(field.surface),
               'cells' : field.surface}
        broadcast_room(id, msg)
