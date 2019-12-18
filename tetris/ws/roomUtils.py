import json
from engine.Room import Room
from web.models import TetrisRoom
# import engine.rooms

active = {}
players = {}
connections = {}


def create_room(id, size):
    active[id] = Room(size)
    players[id] = {}
    for x in range(size):
        players[id][str(x)] = None
    print(active)


def detect_player(conn):
    print(conn.request_headers)
    cookies = conn.request_headers['COOKIE'].split('; ')
    for x in cookies:
        print(x)
        if x.startswith('session_key='):
            from web.models import Session
            key = x.replace('session_key=', '')
            player = Session.objects.get(key=key).user.username
            return player
    return 'guest'


async def broadcast(room, msg):
    for field in room.fields:
        if field.websocket is not None:
            await field.websocket.send(msg)


def init_room(room):
    id = room['id']
    if id in rooms_active:
        msg = 'room exists #' + id
        resp = json.dumps({'type': 'info', 'msg': msg})
        return resp
    rooms_active[id] = Room(int(room['players']))
    rooms_players[id] = {}
    print(rooms_active[id].fields[0].surface)
    for x in range(int(room['players'])):
        rooms_players[id][str(x)] = None
    msg = 'Room created #' + id
    resp = json.dumps({'type': 'info', 'msg': msg})
    return resp


async def connect(conn, data):
    id = data['room_id']
    print(active, id)

    if id not in active:
        msg = 'room does not exist #' + id
        return json.dumps({'type': 'info', 'msg' : msg})
    pos = int(data['pos'])
    if 'player' not in data or data['player'] is None:
        player_name = detect_player(conn)
        await conn.send(json.dumps({'type': 'player', 'player': player_name}))
    else:
        player_name = data['player']
    if conn not in connections:
        if rooms_active[id].fields[pos].websocket is None:
            rooms_active[id].fields[pos].websocket = conn
            rooms_players[id][pos] = player_name
            connections[conn] = id
            msg = 'player ' + player_name + 'entered room # ' + id
            resp = json.dumps({'type': 'connect',
                               'pos': pos,
                               'player': player_name
                               })
            await broadcast(rooms_active[id], resp)
        else:
            msg = 'another player(' + rooms_players[id][pos] + ') at position ' + str(pos) + ' at room # ' + id
    else:
        msg = 'already connected, room # ' + connections[conn]
    return json.dumps({'type': 'info', 'msg': msg})
