import engine.status as status
from engine.Room import Room
from web.models import TetrisRoom, Player, Session

def create_room(id, size):
    new_room = Room(size)
    room_players = {}
    for x in range(size):
        room_players[str(x)] = None
    print('new_room', new_room)
    status.active_rooms[id] = new_room
    status.players[id] = room_players
    print('created engine room # ', str(id))
    print('status', status.active_rooms)


def find_next_id():
    return TetrisRoom.objects.next_id()


def detect_player(conn):
    print('detecting player')
    headers = conn.scope['headers']
    cookies = None
    for x in headers:
        if x[0].decode('utf-8').lower() == 'cookie':
            cookies = x[1].decode('utf-8').split('; ')
            break
    # cookies = conn.request_headers['COOKIE'].split('; ')
    print(cookies)
    for x in cookies:
        # print(x)
        if x.startswith('session_key='):
            key = x.replace('session_key=', '')
            player = Session.objects.get(key=key).user
            print(player)
            return player
    # create new player
    return 'guest'

def make_connect(conn, data):
    id = data['room_id']
    print('active rooms :', status.active_rooms)
    if int(id) not in status.active_rooms:
        msg = 'No room # ' + id
        return {'type': 'info', 'msg': msg}
    else:
        player = detect_player(conn)
        conn.send_json({'type': 'player', 'player': player.username})

        if conn in status.connections:
            msg = 'already connected, room # ' + str(status.connections[conn])
            return {'type': 'info', 'msg': msg}

        pos = int(data['pos'])
        active_room = status.active_rooms[int(id)]
        active_players = status.players[int(id)]
        if active_room.fields[pos].websocket is None:
            active_room.fields[pos].websocket = conn
            active_room.fields[pos].player = player
            active_players[pos] = player.username
            status.connections[conn] = int(id)

            tetris_room = TetrisRoom.objects.get(room_id=int(id))
            print(tetris_room)
            tetris_room.add_player(player, pos)
            msg = 'player ' + player.username + 'entered room # ' + id
            resp = {'type': 'connected',
                               'pos': pos,
                               'player': player.username,
                               'msg' : msg
                               }
        else:
            pl = active_room.fields[pos].player.username
            msg = 'Another player ' + pl + ' at place # ' + str(pos) + ' room ' + id
            resp = {'type': 'info',
                             'msg' : msg}
        return resp
