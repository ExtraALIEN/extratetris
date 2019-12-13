import asyncio
import websockets

async def field_updater_sender(websocket, path, field):
    while True:
        message = await field.updater()
        await websocket.send(message)

start_server = websockets.serve(field_status_sender, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
