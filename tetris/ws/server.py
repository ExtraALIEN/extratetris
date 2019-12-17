import asyncio
import websockets
import json


rooms_active = {}
rooms_players = {}
connections = {}

async def tetris_ws(conn, path):
    async for msg in conn:
        data = json.loads(msg)
        type = data['type']
        if type == 'init':
            await conn.send(init_room(data['room']))
        elif type == 'connect':
            await conn.send(connect(conn, data))
        elif type == 'disconnect':
            await disconnect(conn)
        elif type == 'msg':
            await broadcast(conn, data['msg'])
        else:
            print(data)


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

def init_room(room):
    import requests
    print(room)
    id = room['id']
    if id in rooms_active:
        msg = 'room exists #' + id
        resp = json.dumps({'msg': msg})
        return resp
    rooms_active[id] = {}
    rooms_players[id] = {}

    for x in range(int(room['players'])):
        rooms_active[id][str(x)] = None
        rooms_players[id][str(x)] = None
    msg = 'Room created #' + id
    resp = json.dumps({'msg': msg})
    return resp

def connect(conn, data):
    id = data['room_id']
    if id not in rooms_active:
        return 'room does not exist #'
    pos = data['pos']
    player = detect_player(conn)
    if conn not in connections:
        if rooms_active[id][pos] is None:
            rooms_active[id][pos] = conn
            rooms_players[id][pos] = player
            connections[conn] = id
            return 'player ' + player + 'entered room # ' + id
        else:
            return 'another player(' + rooms_players[id][pos] + ') at position ' + pos + ' at room # ' + id
    else:
        return 'already connected, room # ' + connections[conn]


async def disconnect(conn):
    room_id = connections[conn]
    connections.pop(conn, None)
    rooms_active[room_id].remove(conn)
    await conn.send('disconnected')

async def broadcast(conn, msg):
    if conn in connections:
        for ws in rooms_active[connections[conn]]:
            await ws.send(msg)

start_server = websockets.serve(tetris_ws, "localhost", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
