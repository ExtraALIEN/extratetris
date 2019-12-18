import asyncio
import websockets
import json
from ws.roomUtils import connect
# import engine.rooms


async def tetris_ws(conn, path):
    async for msg in conn:
        data = json.loads(msg)
        print(data)
        type = data['type']
        if type == 'init':
            await conn.send(init_room(data['room']))
        elif type == 'load-room':
            await conn.send(load_room(data['room_id']))
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

# engine.rooms.active = {}
# engine.rooms.players = {}
# engine.rooms.connections = {}

start_server = websockets.serve(tetris_ws, "localhost", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
