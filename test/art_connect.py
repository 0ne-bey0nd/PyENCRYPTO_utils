import socket

server_address = '117.72.8.45'
art_port = 2929
art_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
art_sock.connect((server_address, art_port))

print(f"Connected to {server_address}:{art_port}")


def receive(socket: socket.socket):
    while True:
        data = socket.recv(1024)
        if not data:
            print("EOF received. Connection closed")
            break
        print(f"Received {len(data)} bytes from {server_address}")
        print(f"Data: {data.decode('utf-8')}")
        if socket.fileno() == -1:
            break

def send(socket):
    while True:
        data = input("Info to send[q to quit]: ")
        if data.lower() == 'q':
            socket.sendall(b'q')
            break
        socket.sendall(data.encode('utf-8'))

import threading

receive_thread = threading.Thread(target=receive, args=(art_sock,))
send_thread = threading.Thread(target=send, args=(art_sock,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

art_sock.close()

print("Connection closed")
