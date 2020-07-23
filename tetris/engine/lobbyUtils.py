import engine.status as status


def connect_lobby(conn):
    status.total_lobby.add(conn)


def disconnect_lobby(conn):
    status.total_lobby.remove(conn)


def broadcast_lobby(id, pos=None, **msg):
    data = msg
    data['id'] = id
    data['pos'] = pos
    connections = status.total_lobby.copy()
    for conn in connections:
        conn.send_json(data)
