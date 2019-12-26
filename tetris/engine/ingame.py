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
    msg = {'type': 'start-tetris',
           'fields': room.to_view()
    }
    broadcast_room(id, msg)
    room.start_timers(id)
    del status.ready[id]


def process_command(conn, data):
    from engine.roomUtils import broadcast_room
    command = data['command']
    id = status.connections[conn]['id']
    pos = status.connections[conn]['pos']
    room = status.active_rooms[id]
    field = room.fields[pos]
    if not field.game_over:
        # p = field.active_piece
        # prev = p.to_view()
        # terminated = False
        if command in ['move_left', 'move_right', 'move_down', 'rotate']:
            field.move(command)

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
