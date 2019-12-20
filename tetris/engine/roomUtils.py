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
    cppkies = None
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
            return player
    # create new player
    return 'guest'

def make_connect(conn, data):
    id = data['room_id']
    print(status.active_rooms)
    print(id, type(id))
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
            msg = 'player ' + player.username + 'entered room # ' + id
            resp = {'type': 'connect',
                               'pos': pos,
                               'player': player.username
                               }
            return resp
# def make_connect(conn, data):
#     id = data['room_id']
#     try:
#         active_room = load('room', id=int(id))
#         active_players = load('players', id=int(id))
#         if 'player' not in data or data['player'] is None:
#             player_name = detect_player(conn)
#             await conn.send(json.dumps({'type': 'player', 'player': player_name}))
#         else:
#             player_name = data['player']
#         if conn in connections:
#             msg = 'already connected, room # ' + str(connections[conn])
#             return json.dumps({'type': 'info', 'msg': msg})
#         else:
#             pos = int(data['pos'])
#             if active_room.fields[pos].websocket is None:
#                 active_room.fields[pos].websocket = conn
#                 active_players[pos] = player_name
#                 connections[conn] = int(id)
#                 save(active_room, 'room', id=int(id))
#                 save(active_players, 'players', id=int(id))
#                 msg = 'player ' + player_name + 'entered room # ' + id
#                 resp = json.dumps({'type': 'connect',
#                                    'pos': pos,
#                                    'player': player_name
#                                    })
#                 return broadcast(active_room, resp)
#             else:
#                 msg = 'another player(' + active_players[pos] + ') at position ' + str(pos) + ' at room # ' + id
#                 return json.dumps({'type': 'info', 'msg': msg})
#     except Error:
#         msg = "Error while connecting, room # " + id
#         return json.dumps({'type': 'info', 'msg': msg})
