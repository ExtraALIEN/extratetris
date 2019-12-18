import json
from engine.Room import Room


rooms_active = {}
rooms_players = {}
connections = {}


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


def init_room(room):
    print(room)
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
    print(resp)
    return resp


async def connect(conn, data):
    id = data['room_id']
    if id not in rooms_active:
        return 'room does not exist #'
    pos = int(data['pos'])
    if 'player' not in data or data['player'] is None:
        player = detect_player(conn)
        await conn.send(json.dumps({'type': 'player', 'player': player}))
    else:
        player = data['player']
    if conn not in connections:
        if rooms_active[id].fields[pos].websocket is None:
            rooms_active[id].fields[pos].websocket = conn
            rooms_players[id][pos] = player
            connections[conn] = id
            msg = 'player ' + player + 'entered room # ' + id
        else:
            msg = 'another player(' + rooms_players[id][pos] + ') at position ' + str(pos) + ' at room # ' + id
    else:
        msg = 'already connected, room # ' + connections[conn]
    return json.dumps({'type': 'info', 'msg': msg})
