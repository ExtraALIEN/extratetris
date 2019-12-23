import engine.status as status

def init_fields(id):
    from engine.roomUtils import broadcast_room
    room = status.active_rooms[id]
    msg = {'type': 'get-ready'}
    broadcast_room(id, msg)

def add_ready(conn):
    id = status.connections[conn]['id']
    if id not in status.ready:
        status.ready[id] = set()
    status.ready[id].add(conn)
    if status.all_ready(id):
        start(id)

def start(id):
    from engine.roomUtils import broadcast_room
    room = status.active_rooms[id]
    fieldsData = [{ x : {
                        'surface': room.fields[x].surface,
                        'queue' : room.fields[x].queue_to_view(),
                        'active_piece' : room.fields[x].active_piece_to_view()
                    }
            } for x in range(len(room.fields))]
    msg = {'type': 'start-tetris',
           'fields': fieldsData
    }
    del status.ready[id]
    broadcast_room(id, msg)
