import engine.status as status
from engine.ListMethods import diff_obj

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
    fieldsData = { x : {
                        'surface': room.fields[x].surface[0:-1],
                        'queue' : room.fields[x].queue_to_view(),
                        'active_piece' : room.fields[x].active_piece_to_view()
                    }
             for x in range(len(room.fields))}
    msg = {'type': 'start-tetris',
           'fields': fieldsData
    }
    del status.ready[id]
    broadcast_room(id, msg)


def process_command(conn, data):
    from engine.roomUtils import broadcast_room
    print(status.connections)
    command = data['command']
    id = status.connections[conn]['id']
    pos = status.connections[conn]['pos']
    room = status.active_rooms[id]
    field = room.fields[pos]
    p = field.active_piece
    prev = p.to_view()
    if command == 'move_left':
        p.move_left()
    elif command == 'move_right':
        p.move_right()
    elif command == 'move_down':
        p.move_down()
    elif command == 'rotate':
        p.rotate()
    cur = p.to_view()
    changes = diff_obj(prev, cur)
    upd = {'type': 'field-update',
           'pos' : pos,
           'changes': changes}
    broadcast_room(id, upd)
    c = field.active_piece
    if c is not p:
        changes = c.to_view()
        changes_copy = c.to_view()
        for y in changes_copy:
            for x in changes_copy[y]:
                if changes_copy[y][x] == 0:
                    del changes[y][x]

        upd = {'type': 'field-update',
                'pos' : pos,
                'changes': changes}
        broadcast_room(id, upd)
