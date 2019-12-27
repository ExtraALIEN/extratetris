import engine.status as status
from engine.Room import Room
from web.models import TetrisRoom, Player, Session
from engine.ingame import init_fields

def create_room(id, size):
    new_room = Room(size)
    activate_room(id, new_room)


def find_next_id():
    return TetrisRoom.objects.next_id()

def detect_player(conn):
    headers = conn.scope['headers']
    cookies = None
    for x in headers:
        if x[0].decode('utf-8').lower() == 'cookie':
            cookies = x[1].decode('utf-8').split('; ')
            break
    for x in cookies:
        if x.startswith('session_key='):
            key = x.replace('session_key=', '')
            try:
                player = Session.objects.get(key=key).user
                return player
            except Session.DoesNotExist:
                return None

def init_room(conn, data):
    id = int(data['room_id'])
    enter_room_lobby(id, conn)
    room = status.active_rooms[id]
    for field in room.fields:
        if field.player is not None:
            upd = {'type': 'update-players',
                               'pos': field.pos,
                               'player': field.player.username
                                }
            broadcast_room(id, upd)

def room_connect(conn, data):
    id = int(data['room_id'])
    player = detect_player(conn)
    conn.send_json({'type': 'player', 'player': player.username})
    if player_in_game(player):
        msg = 'already connected, room # ' + str(status.players[player]['id'])
        conn.send_json({'type': 'info', 'msg': msg})
    else:
        pos = int(data['pos'])
        if field_avalaible(id, pos):
            enter_field(id, pos, conn, player)
            tetris_room = TetrisRoom.objects.get(room_id=int(id))
            tetris_room.add_player(player, pos)
            msg = 'player ' + player.username + 'entered room # ' + str(id)
            upd = {'type': 'update-players',
                                   'pos': pos,
                                   'player': player.username,
                                    }
            resp = {'type': 'connected',
                                   'pos': pos,
                                   'player': player.username,
                                   'msg' : msg
                                   }
            broadcast_room(int(id), upd)
            conn.send_json(resp)
            if tetris_room.is_full():
                tetris_room.start()
                start_signal = {'type': 'start-game'}
                broadcast_room(int(id), start_signal)
                init_fields(int(id))
        else:
            msg = 'Another player ' + ' at place # ' + str(pos) + ' room ' + id
            resp = {'type': 'info', 'msg': msg}
            conn.send_json(resp)

def room_disconnect(conn, data):
    player = detect_player(conn)
    exit_field(conn)
    id = int(data['room_id'])
    pos = int(data['pos'])
    tetris_room = TetrisRoom.objects.get(room_id=id)
    tetris_room.remove_player(player, pos)
    if not tetris_room.started:
        dis = {'type': 'disconnect-player', 'pos': pos}
        broadcast_room(id, dis)



def room_hard_disconnect(conn):
    player = detect_player(conn)
    id = status.in_room_lobby[conn]
    tetris_room = TetrisRoom.objects.get(room_id=id)
    exit_room_lobby(conn)
    if not tetris_room.started:
        if player == tetris_room.author:
            delete = {'type': 'room-deleted'}
            broadcast_room(id, delete)
            all_exit_fields(id)
            all_exit_room_lobby(id)
            deactivate_room(id)
            tetris_room.delete()
        elif player_in_game(player):
            pos = status.players[player]['pos']
            data = {'room_id': id, 'pos': pos}
            room_disconnect(conn, data)
    else:
        if player_in_game(player):   # player was in game
            room = status.active_rooms[id]
            pos = status.players[player]['pos']
            room.fields[pos].end_game(hard_disconnect=True)
            dis = {'type': 'game-disconnect', 'pos': pos}
            broadcast_room(id, dis)
            data = {'room_id': id, 'pos': pos}
            room_disconnect(conn, data)
    if player.is_guest:
        player.delete()




def broadcast_room(room_id, data):
    for conn in status.room_lobby[room_id]:
        conn.send_json(data)

def activate_room(id, room_instance):
    status.active_rooms[int(id)] = room_instance
    create_room_lobby(id)

def deactivate_room(id):
    delete_room_lobby(id)
    del status.active_rooms[int(id)]

def create_room_lobby(id):
    status.room_lobby[int(id)] = set()

def delete_room_lobby(id):
    del status.room_lobby[int(id)]

def room_lobby_exists(id):
    return int(id) in status.room_lobby


def enter_room_lobby(id, conn):
    status.in_room_lobby[conn] = int(id)
    status.room_lobby[int(id)].add(conn)

def exit_room_lobby(conn):
    id = status.in_room_lobby[conn]
    status.room_lobby[id].remove(conn)
    del status.in_room_lobby[conn]


def all_exit_room_lobby(id):
    lobby_copy = set(status.room_lobby[id])
    for ws in lobby_copy:
        exit_room_lobby(ws)

def enter_field(id, pos, conn, player):
    room = status.active_rooms[int(id)]
    room.fields[int(pos)].websocket = conn
    room.fields[int(pos)].player = player
    status.connections[conn] = {'id': int(id), 'pos': int(pos)}
    status.players[player] = {'id': int(id), 'pos': int(pos)}

def exit_field(conn):
    data = status.connections[conn]
    id = data['id']
    pos = data['pos']
    room = status.active_rooms[id]
    field = room.fields[pos]
    field.websocket = None
    pl = field.player
    field.player = None
    del status.connections[conn]
    del status.players[pl]


def all_exit_fields(id):
    room = status.active_rooms[int(id)]
    for field in room.fields:
        if field.websocket is not None:
            exit_field(field.websocket)

def player_in_game(player):
    return player in status.players

def field_avalaible(id, pos):
    room = status.active_rooms[int(id)]
    return room.fields[int(pos)].websocket is None
