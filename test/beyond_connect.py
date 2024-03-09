import socket

server_address = '117.72.8.45'
beyond_port = 5252
beyond_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
beyond_sock.connect((server_address, beyond_port))



print(f"Connected to {server_address}:{beyond_port}")


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

receive_thread = threading.Thread(target=receive, args=(beyond_sock,))
send_thread = threading.Thread(target=send, args=(beyond_sock,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

beyond_sock.close()

print("Connection closed")
