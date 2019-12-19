import cloudpickle
from web.models import TetrisRoom, BitRoom, BitPlayers, BitConnection


def save(obj, type, id):
    bin = cloudpickle.dumps(obj)
    if type == 'room':
        new_room = BitRoom(room_number=id, raw_data=bin)
        new_room.save()
    elif type == 'players':
        new_players_dict = BitPlayers(room_number=id, raw_data=bin)
        new_players_dict.save()
    elif type == 'conn':
        conn_data = BitConnection(raw_data=bin, room_number=id )


def load(type, id=None):
    obj = None
    if type == 'room':
        obj = BitRoom.objects.get(room_number=id)
    elif type == 'players':
        obj = BitPlayers.objects.get(room_number=id)
    print(obj)
    return cloudpickle.loads(obj.raw_data)

def findConnectionRoom(conn):
    bin = cloudpickle.dumps(conn)
    obj = BitConnection.objects.get(raw_data=bin)
    return obj
