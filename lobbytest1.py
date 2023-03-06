import socket
import threading

PORT = 1234 # порт, на котором сервер принимает соединения

lobbies = {}
clients = {}

class Lobby:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, conn, addr, name):
        self.clients.append((conn, addr, name))
        clients[addr] = self

    def remove_client(self, conn, addr):
        self.clients.remove((conn, addr, clients[addr]))
        del clients[addr]

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if data.startswith('join '):
                name = data[5:].strip()
                lobby = lobbies.get(name)
                if lobby is None:
                    lobby = Lobby(name)
                    lobbies[name] = lobby
                lobby.add_client(conn, addr, name)
                print(f'{addr} joined lobby "{name}"')
            elif data.startswith('leave'):
                lobby = clients[addr]
                lobby.remove_client(conn, addr)
                print(f'{addr} left lobby "{lobby.name}"')
            elif data.startswith('list'):
                lobbies_str = ', '.join([lobby.name for lobby in lobbies.values()])
                conn.sendall(f'Lobbies: {lobbies_str}'.encode())
            elif data.startswith('quit'):
                break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()
    print('Server started on port', PORT)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
