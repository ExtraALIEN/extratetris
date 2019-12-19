import json
from engine.Room import Room
from web.models import TetrisRoom
# import engine.rooms
from ws.dbio import save, load, findConnectionRoom

active = {}
players = {}
connections = {}


def create_room(id, size):
    active_room = Room(size)
    active_players = {}
    for x in range(size):
        active_players[str(x)] = None
    print(active_room)
    save(active_room, 'room', id=id)
    save(active_players, 'players', id=id)



def detect_player(conn):
    # print(conn.request_headers)
    cookies = conn.request_headers['COOKIE'].split('; ')
    for x in cookies:
        # print(x)
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


async def make_connect(conn, data):
    id = data['room_id']
    print(connections, id)
    try:
        active_room = load('room', id=int(id))
        active_players = load('players', id=int(id))
        if 'player' not in data or data['player'] is None:
            player_name = detect_player(conn)
            await conn.send(json.dumps({'type': 'player', 'player': player_name}))
        else:
            player_name = data['player']
        if conn in connections:
            msg = 'already connected, room # ' + str(connections[conn])
            return json.dumps({'type': 'info', 'msg': msg})
        else:
            pos = int(data['pos'])
            if active_room.fields[pos].websocket is None:
                active_room.fields[pos].websocket = conn
                active_players[pos] = player_name
                connections[conn] = int(id)
                save(active_room, 'room', id=int(id))
                save(active_players, 'players', id=int(id))
                msg = 'player ' + player_name + 'entered room # ' + id
                resp = json.dumps({'type': 'connect',
                                   'pos': pos,
                                   'player': player_name
                                   })
                return await broadcast(active_room, resp)
            else:
                msg = 'another player(' + active_players[pos] + ') at position ' + str(pos) + ' at room # ' + id
                return json.dumps({'type': 'info', 'msg': msg})
    except Error:
        msg = "Error while connecting, room # " + id
        return json.dumps({'type': 'info', 'msg': msg})
