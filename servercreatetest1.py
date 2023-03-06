import socket
import threading

PORT = 1234 # порт, на котором сервер принимает соединения

clients = []

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        clients.append(addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received message:', data.decode())
            for client in clients:
                if client != addr:
                    conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()
    print('Server started on port', PORT)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
