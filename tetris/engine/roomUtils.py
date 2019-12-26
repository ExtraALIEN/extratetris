import engine.status as status
from engine.Room import Room
from web.models import TetrisRoom, Player, Session
from engine.ingame import init_fields

def create_room(id, size):
    new_room = Room(size)
    status.active_rooms[id] = new_room
    status.room_lobby[id] = set()


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

def room_connect(conn, data):
    id = data['room_id']
    if int(id) not in status.active_rooms:
        msg = 'No room # ' + id
        conn.send_json({'type': 'info', 'msg': msg})
    else:
        player = detect_player(conn)
        conn.send_json({'type': 'player', 'player': player.username})
        for p in status.players:
            print(p.login, status.players[p])
        if player in status.players:
            msg = 'already connected, room # ' + str(status.players[player]['id'])
            conn.send_json({'type': 'info', 'msg': msg})
        else:
            pos = int(data['pos'])
            active_room = status.active_rooms[int(id)]
            if active_room.fields[pos].websocket is None:
                active_room.fields[pos].websocket = conn
                active_room.fields[pos].player = player
                status.connections[conn] = {'id': int(id), 'pos': pos}
                status.players[player] = {'id': int(id), 'pos': pos}
                tetris_room = TetrisRoom.objects.get(room_id=int(id))
                tetris_room.add_player(player, pos)
                msg = 'player ' + player.username + 'entered room # ' + id
                upd = {'type': 'update-players',
                                   'pos': pos,
                                   'player': player.username,
                                    }
                broadcast_room(int(id), upd)
                resp = {'type': 'connected',
                                   'pos': pos,
                                   'player': player.username,
                                   'msg' : msg
                                   }
                conn.send_json(resp)
                if tetris_room.is_full():
                    tetris_room.start()
                    start_signal = {'type': 'start-game'}
                    broadcast_room(int(id), start_signal)
                    init_fields(int(id))

            else:
                pl = active_room.fields[pos].player.username
                msg = 'Another player ' + pl + ' at place # ' + str(pos) + ' room ' + id
                resp = {'type': 'info',
                                 'msg' : msg}
                conn.send_json(resp)


def init_room(conn, data):
    id = int(data['room_id'])

    room = status.active_rooms[id]
    enter_room(id, conn)
    print('entered, ', id, status.room_lobby[id])
    for x in range(len(room.fields)):
        field = room.fields[x]
        if field.player is not None:
            upd = {'type': 'update-players',
                               'pos': x,
                               'player': field.player.username
                                }
            broadcast_room(id, upd)


def room_hard_disconnect(conn):
    player = detect_player(conn)
    id = status.in_room_lobby[conn]
    exit_room(id, conn)
    pos = None
    if conn in status.connections:
        pos = status.connections[conn]['pos']

    tetris_room = TetrisRoom.objects.get(room_id=id)
    if not tetris_room.started:
        if player == tetris_room.author:
            delete = {'type': 'room-deleted'}
            broadcast_room(id, delete)
            lobby_copy = set(status.room_lobby[id])
            for ws in lobby_copy:
                exit_room(id, ws)
                if ws in status.connections:
                    pos = status.connections[ws]['pos']
                    data = {'room_id': id, 'pos': pos}
                    room_disconnect(ws, data)
            del status.room_lobby[id]
            del status.active_rooms[id]
            tetris_room.delete()
        elif conn in status.connections:
            pos = status.connections[conn]['pos']
            data = {'room_id': id, 'pos': pos}
            room_disconnect(conn, data)
    else:
        if pos is not None:   # player was in game
            room = status.active_rooms[id]
            print(player.login, id, status.active_rooms)
            room.fields[pos].end_game()
            dis = {'type': 'game-disconnect', 'pos': pos}
            broadcast_room(id, dis)
            data = {'room_id': id, 'pos': pos}
            room_disconnect(conn, data)
    if player.is_guest:
        player.delete()


def room_disconnect(conn, data):
    id = int(data['room_id'])
    pos = int(data['pos'])
    active_room = status.active_rooms[id]
    active_room.fields[pos].websocket = None

    player = active_room.fields[pos].player
    active_room.fields[pos].player = None

    del status.connections[conn]
    del status.players[player]
    tetris_room = TetrisRoom.objects.get(room_id=int(id))
    tetris_room.remove_player(player, pos)
    dis = {'type': 'disconnect-player', 'pos': pos}
    broadcast_room(id, dis)
    if player.is_guest:
        print('guest disconnected ', player.login)



def enter_room(id, conn):
    status.room_lobby[id].add(conn)
    status.in_room_lobby[conn] = id

def exit_room(id, conn):
    status.room_lobby[id].remove(conn)
    del status.in_room_lobby[conn]
    print('in room lobby: ', status.in_room_lobby)

def broadcast_room(room_id, data):
    for conn in status.room_lobby[room_id]:
        conn.send_json(data)
