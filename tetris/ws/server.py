import asyncio
import websockets
import json

rooms_entered = {}
socket_room = {}

async def tetris_ws(websocket, path):
    async for msg in websocket:
        data = json.loads(msg)
        if data['type'] == 'connect':
            await websocket.send(connect(websocket, data['room_id']))
        elif data['type'] == 'disconnect':
            await disconnect(websocket)
        elif data['type'] == 'msg':
            await broadcast(websocket, data['msg'])


def connect(websocket, room_id):
    if room_id not in rooms_entered:
        rooms_entered[room_id] = set()
    if not websocket in socket_room:
        rooms_entered[room_id].add(websocket)
        socket_room[websocket] = room_id
        return 'entered room # '+ room_id
    else:
        return 'already connected, room # '+ socket_room[websocket]


async def disconnect(websocket):
    room_id = socket_room[websocket]
    socket_room.pop(websocket, None)
    rooms_entered[room_id].remove(websocket)
    await websocket.send('disconnected')

async def broadcast(websocket, msg):
    if websocket in socket_room:
        for ws in rooms_entered[socket_room[websocket]]:
            await ws.send(msg)

start_server = websockets.serve(tetris_ws, "localhost", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
