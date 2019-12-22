import engine.status as status
from engine.Room import Room
from web.models import TetrisRoom, Player, Session
from engine.ingame import init_fields

def create_room(id, size):
    new_room = Room(size)
    print('new_room', new_room)
    status.active_rooms[id] = new_room
    status.room_lobby[id] = set()
    print('created engine room # ', str(id))
    print('status', status.active_rooms)


def find_next_id():
    return TetrisRoom.objects.next_id()

def enter_room(id, conn):
    status.room_lobby[id].add(conn)

def exit_room(id, conn):
    status.room_lobby[id].remove(conn)

def detect_player(conn, id):
    print('detecting player')
    headers = conn.scope['headers']
    cookies = None
    player = None
    for x in headers:
        if x[0].decode('utf-8').lower() == 'cookie':
            cookies = x[1].decode('utf-8').split('; ')
            break
    for x in cookies:
        if x.startswith('session_key='):
            key = x.replace('session_key=', '')
            print('find session, key= ', key)
            try:
                player = Session.objects.get(key=key).user
                return player
            except Session.DoesNotExist:
                pass
    if player is None:
        url = '/room/'+str(id)+'/'
        guest = Player.objects.create_guest()
        guest.do_login(url=url)
        return guest


def make_connect(conn, data):
    id = data['room_id']
    print('active rooms :', status.active_rooms)
    if int(id) not in status.active_rooms:
        msg = 'No room # ' + id
        conn.send_json({'type': 'info', 'msg': msg})
    else:
        player = detect_player(conn, id=id)
        print('player= ', player.login)
        conn.send_json({'type': 'player', 'player': player.username})

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
                print(tetris_room)
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
    print(conn)
    id = int(data['room_id'])
    print(id, status.active_rooms)
    room = status.active_rooms[id]
    enter_room(id, conn)
    for x in range(len(room.fields)):
        field = room.fields[x]
        if field.player is not None:
            upd = {'type': 'update-players',
                               'pos': x,
                               'player': field.player.username
                                }
            broadcast_room(id, upd)


def room_disconnect(conn, data):
    id = None
    pos = None
    if data is not False:
        id = int(data['room_id'])
        pos = int(data['pos'])
    else:
        if conn in status.connections:
            id = status.connections[conn]['id']
            pos = status.connections[conn]['pos']
            exit_room(id, conn)
    active_room = status.active_rooms[id]
    active_room.fields[pos].websocket = None
    player_to_remove = active_room.fields[pos].player
    active_room.fields[pos].player = None
    del status.connections[conn]
    del status.players[player_to_remove]
    tetris_room = TetrisRoom.objects.get(room_id=int(id))
    tetris_room.remove_player(player_to_remove, pos)
    dis = {'type': 'disconnect-player',
                   'pos': pos}
    broadcast_room(id, dis)
    if data is False:
        print(Player.objects.all().count())
        print('removing player')
        player_to_remove.delete()
        tetris_room.delete()
        print(Player.objects.all().count())

def broadcast_room(room_id, data):
    for conn in status.room_lobby[room_id]:
        conn.send_json(data)
