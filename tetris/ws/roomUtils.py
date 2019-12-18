import json
import pickle
from engine.Room import Room
from web.models import TetrisRoom, BitRoom, BitPlayers, BitConnection
# import engine.rooms

active = {}
players = {}
connections = {}


def create_room(id, size):
    active_room = Room(size)
    active_players = {}
    for x in range(size):
        active_players[str(x)] = None
    print(active_room)
    r = pickle.dumps(active_room)
    new_r = BitRoom(room_number=id, raw_data=r)
    new_r.save()
    p = pickle.dumps(active_players)
    new_p = BitPlayer(room_number=id, raw_data=p)
    new_p.save()



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
    r = None
    p = None
    try:
        r = BitRoom.objects.get(room_number=int(id))
        p = BitPlayers.objects.get(room_number=int(id))
        import pickle
        active_room = pickle.loads(r)
        active_players = pickle.loads(p)
        pos = int(data['pos'])
        if 'player' not in data or data['player'] is None:
            player_name = detect_player(conn)
            await conn.send(json.dumps({'type': 'player', 'player': player_name}))
        else:
            player_name = data['player']
        c = pickle.dumps(conn)
        try:
            connected = BitConnection.objects.get(conn=c)
            msg = 'already connected, room # ' + str(connected.room_number)
            return json.dumps({'type': 'info', 'msg': msg})
        except Error:
            if active_room.fields[pos].websocket is None:
                active_room.fields[pos].websocket = conn
                active_players[pos] = player_name
                connected.room_number = int(id)
                msg = 'player ' + player_name + 'entered room # ' + id
                resp = json.dumps({'type': 'connect',
                                   'pos': pos,
                                   'player': player_name
                                   })
                # make dumps
                r.save()
                p.save()
                c.save()
                await broadcast(active_room, resp)
            else:
                msg = 'another player(' + active_players[pos] + ') at position ' + str(pos) + ' at room # ' + id
                return json.dumps({'type': 'info', 'msg': msg})
