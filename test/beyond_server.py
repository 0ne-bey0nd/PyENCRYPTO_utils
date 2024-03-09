# beyond server
import socket


server_address = '0.0.0.0'

art_port = 2929
art_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
art_sock.bind((server_address, art_port))

beyond_port = 5252
beyond_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
beyond_sock.bind((server_address, beyond_port))

art_sock.listen(1)
beyond_sock.listen(1)

art_conn, art_addr = art_sock.accept()
beyond_conn, beyond_addr = beyond_sock.accept()

ART = 0
BEYOND = 1

def get_name_from_role(role):
    if role == ART:
        return "ART"
    elif role == BEYOND:
        return "BEYOND"
    else:
        raise ValueError(f"Invalid role {role}")


print(f"Connected to {art_addr} and {beyond_addr}")

def receive_and_send(socket_in, socket_out, in_role, out_role):
    peer_name_in = socket_in.getpeername()
    peer_name_out = socket_out.getpeername()
    while True:
        data = socket_in.recv(1024)
        if data == b'q':
            if socket_out.fileno() != -1:
                socket_out.sendall(b'The other side has quit')
            socket_in.sendall(b'')
            socket_in.close()
            print(f"Connection closed by {peer_name_in}")

            # TODO: 线程间通信，在更新完socket_in之后，通知另一个线程更新socket_out
            if in_role == ART:
                socket_in, _ = art_sock.accept()
            elif in_role == BEYOND:
                socket_in, _ = beyond_sock.accept()
            else:
                raise ValueError(f"Invalid role {in_role}")

        elif socket_out.fileno() == -1:
            socket_in.sendall(b'The other side is not connected')
        else:
            socket_out.sendall(data)
            print(f"Send {len(data)} bytes from {peer_name_in} to {peer_name_out}")
            print(f"Data: {data.decode('utf-8')}")

# 将两个socket连接起来，同时接收数据，然后发送数据
import threading

art_to_beyond = threading.Thread(target=receive_and_send, args=(art_conn, beyond_conn, ART, BEYOND))
beyond_to_art = threading.Thread(target=receive_and_send, args=(beyond_conn, art_conn, BEYOND, ART))

art_to_beyond.start()
beyond_to_art.start()

art_to_beyond.join()
beyond_to_art.join()

art_conn.close()
beyond_conn.close()

art_sock.close()
beyond_sock.close()

print("Connection closed")
