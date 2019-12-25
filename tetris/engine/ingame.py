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
                        'queue' : room.fields[x].queue.to_view(),
                        'active_piece' : room.fields[x].active_piece.to_view()
                    }
             for x in range(len(room.fields))}
    msg = {'type': 'start-tetris',
           'fields': fieldsData
    }
    del status.ready[id]
    room.start_timers(id)
    broadcast_room(id, msg)


def process_command(conn, data):
    from engine.roomUtils import broadcast_room
    command = data['command']
    id = status.connections[conn]['id']
    pos = status.connections[conn]['pos']
    room = status.active_rooms[id]
    field = room.fields[pos]
    if not field.game_over:
        p = field.active_piece
        prev = p.to_view()
        terminated = False
        if command == 'move_left':
            p.move_left()
        elif command == 'move_right':
            p.move_right()
        elif command == 'move_down':
            terminated = p.move_down()
            p.field.speed += p.field.speed_boost
        elif command == 'rotate':
            p.rotate()
        cur = p.to_view()
        changes = diff_obj(prev, cur)
        upd = {'type': 'field-update',
               'pos' : pos,
               'changes': changes}
        broadcast_room(id, upd)
        if terminated:
            print('terminated')
            changes = {y: {x:field.surface[y][x] for x in range(len(field.surface[y]))}  \
                            for y in range(len(field.surface)-1)}
            field_upd = {'type': 'field-update',
                          'changes': changes,
                          'pos': pos}
            broadcast_room(id, field_upd)
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
    else:
        conn.send_json({'type': 'game-over'});

def auto_move_down(field):
    from engine.roomUtils import broadcast_room
    id = status.connections[field.websocket]['id']
    pos = status.connections[field.websocket]['pos']
    p = field.active_piece
    prev = p.to_view()
    terminated = p.move_down()
    cur = p.to_view()
    changes = diff_obj(prev, cur)
    upd = {'type': 'field-update',
           'pos' : pos,
           'changes': changes}
    broadcast_room(id, upd)
    if terminated:
        changes = {y: {x:field.surface[y][x] for x in range(len(field.surface[y]))}  \
                        for y in range(len(field.surface)-1)}
        field_upd = {'type': 'field-update',
                      'changes': changes,
                      'pos': pos}
        broadcast_room(id, field_upd)
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
