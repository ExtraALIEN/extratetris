import asyncio
import websockets
import json
from ws.roomUtils import init_room, connect


async def tetris_ws(conn, path):
    async for msg in conn:
        data = json.loads(msg)
        type = data['type']
        if type == 'init':
            await conn.send(init_room(data['room']))
        elif type == 'connect':
            await conn.send(await connect(conn, data))
        elif type == 'disconnect':
            await disconnect(conn)
        elif type == 'msg':
            await broadcast(conn, data['msg'])
        else:
            print(data)


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
