import socket


def _Connect(address: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    return sock


def _Listen(address: str, port: int) -> socket.socket:
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind((address, port))
    listen_sock.listen(1)
    return listen_sock.accept()[0]


def Listen(address: str, port: int, sockets: list[list], numConnections: int, myID: int) -> bool:
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind((address, port))
    listen_socket.listen(1)
    for i in range(numConnections):
        sock = listen_socket.accept()[0]
        nID = int.from_bytes(sock.recv(4), "little")
        conID = int.from_bytes(sock.recv(4), "little")
        if nID >= len(sockets):
            sock.close()
            i -= 1
            continue
        if conID >= len(sockets[myID]):
            sock.close()
            i -= 1
            continue
        sockets[nID][conID] = sock
    return True


def Connect(address: str, port: int, sockets: list, id: int) -> bool:
    for j in range(len(sockets)):
        sockets[j] = _Connect(address, port)
        if sockets[j]:
            sockets[j].send(id.to_bytes(4, "little"))
            index = j.to_bytes(4, "little")
            sockets[j].send(index)
        else:
            return False
    return True
