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
    room.start_timers()
    del status.ready[id]


def process_command(conn, data):
    from engine.roomUtils import broadcast_room
    command = data['command']
    id = status.connections[conn]['id']
    pos = status.connections[conn]['pos']
    room = status.active_rooms[id]
    field = room.fields[pos]
    if field is not None and not field.game_over:
        # p = field.active_piece
        # prev = p.to_view()
        # terminated = False
        if command in ['move_left', 'move_right', 'move_down', 'rotate']:
            field.move(command)
