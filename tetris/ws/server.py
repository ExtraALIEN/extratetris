import asyncio
import websockets
import json

rooms_entered = {}
connections = {}

async def tetris_ws(conn, path):
    async for msg in conn:
        data = json.loads(msg)
        if data['type'] == 'connect':
            await conn.send(connect(conn, data['room_id']))
        elif data['type'] == 'disconnect':
            await disconnect(conn)
        elif data['type'] == 'msg':
            await broadcast(conn, data['msg'])


def connect(conn, room_id):
    if room_id not in rooms_entered:
        rooms_entered[room_id] = set()
    if not conn in connections:
        rooms_entered[room_id].add(conn)
        connections[conn] = room_id
        return 'entered room # '+ room_id
    else:
        return 'already connected, room # '+ connections[conn]


async def disconnect(conn):
    room_id = connections[conn]
    connections.pop(conn, None)
    rooms_entered[room_id].remove(conn)
    await conn.send('disconnected')

async def broadcast(conn, msg):
    if conn in connections:
        for ws in rooms_entered[connections[conn]]:
            await ws.send(msg)

start_server = websockets.serve(tetris_ws, "localhost", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
