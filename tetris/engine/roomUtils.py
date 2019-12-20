import engine.status as status
from engine.Room import Room

def create_room(id, size):
    new_room = Room(size)
    room_players = {}
    for x in range(size):
        room_players[str(x)] = None
    print('new_room', new_room)
    status.active_rooms[id] = new_room
    status.players[id] = room_players
    print('status', status.active_rooms)


def make_connect(conn, data):
    id = data['room_id']
    if id not in status.active_rooms:
        msg = 'No room'
        return ({'type': 'info', 'msg': msg})
    else:
        msg = 'Room exists'
        return ({'type': 'info', 'msg': msg})
# def make_connect(conn, data):
#     id = data['room_id']
#     try:
#         active_room = load('room', id=int(id))
#         active_players = load('players', id=int(id))
#         if 'player' not in data or data['player'] is None:
#             player_name = detect_player(conn)
#             await conn.send(json.dumps({'type': 'player', 'player': player_name}))
#         else:
#             player_name = data['player']
#         if conn in connections:
#             msg = 'already connected, room # ' + str(connections[conn])
#             return json.dumps({'type': 'info', 'msg': msg})
#         else:
#             pos = int(data['pos'])
#             if active_room.fields[pos].websocket is None:
#                 active_room.fields[pos].websocket = conn
#                 active_players[pos] = player_name
#                 connections[conn] = int(id)
#                 save(active_room, 'room', id=int(id))
#                 save(active_players, 'players', id=int(id))
#                 msg = 'player ' + player_name + 'entered room # ' + id
#                 resp = json.dumps({'type': 'connect',
#                                    'pos': pos,
#                                    'player': player_name
#                                    })
#                 return broadcast(active_room, resp)
#             else:
#                 msg = 'another player(' + active_players[pos] + ') at position ' + str(pos) + ' at room # ' + id
#                 return json.dumps({'type': 'info', 'msg': msg})
#     except Error:
#         msg = "Error while connecting, room # " + id
#         return json.dumps({'type': 'info', 'msg': msg})
