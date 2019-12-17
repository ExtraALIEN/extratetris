import asyncio
import websockets
import json

rooms_active = {}
connections = {}

async def tetris_ws(conn, path):
    async for msg in conn:
        data = json.loads(msg)
        if data['type'] == 'init-room':
            await conn.send(init_room(data['room']))
        elif data['type'] == 'connect':
            await conn.send(connect(conn, data))
        elif data['type'] == 'disconnect':
            await disconnect(conn)
        elif data['type'] == 'msg':
            await broadcast(conn, data['msg'])
        else:
            print(data)


def init_room(room):
    print(room)
    id = room['id']
    if id in rooms_active:
        return 'room exists #'+ id
    rooms_active[id] = {}
    for x in range(int(room['players'])):
        rooms_active[id][str(x)] = None
    print(rooms_active)
    return 'Room created #' + id

def connect(conn, data):
    id = data['room_id']
    if id not in rooms_active:
        return 'room does not exist #'
    pos = data['pos']
    if conn not in connections:
        if rooms_active[id][pos] is None:
            rooms_active[id][pos] = conn
            connections[conn] = id
            return 'entered room # ' + id
        else:
            return 'another player at position ' + pos + ' at room # ' + id
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
