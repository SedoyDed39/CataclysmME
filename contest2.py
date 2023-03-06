import socket

PORT = 1234 # порт, на котором сервер принимает соединения

host = input('Enter server IP address: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, PORT))
    print('Connected to server')
    while True:
        message = input('Enter a message: ')
        s.sendall(message.encode())
        data = s.recv(1024)
        print('Received message:', data.decode())
