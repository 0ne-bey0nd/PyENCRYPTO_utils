import socket
from typing import Optional, Tuple, Any

from PyENCRYPTO_utils.typedefs import RETRY_CONNECT
import time


# std::unique_ptr<CSocket> Listen(const std::string& address, uint16_t port) {
# 	auto listen_socket = std::make_unique<CSocket>();
# 	if (!listen_socket->Bind(address, port)) {
# 		return nullptr;
# 	}
# 	if (!listen_socket->Listen()) {
# 		return nullptr;
# 	}
# 	return listen_socket->Accept();
# }

def listen(address: str, port: int) -> Optional[tuple[socket.socket, Any]]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((address, port))
        sock.listen(1)
        return sock.accept()
    except OSError:
        return None


def connect(address: str, port: int) -> Optional[socket.socket]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for i in range(RETRY_CONNECT):
        try:
            sock.connect((address, port))
            return sock
        except ConnectionRefusedError:
            time.sleep(0.01)
        print("Connect failed due to timeout!")
    return None


class Socket(object):
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def send(self, data: bytes) -> None:
        self.sock.sendall(data)

    def recv(self, size: int) -> bytes:
        return self.sock.recv(size)

    def _send_c_int(self, data: int, size: int) -> None:
        assert data >= 0
        self.send(data.to_bytes(size, "little"))

    def _recv_c_int(self, size: int) -> int:
        return int.from_bytes(self.sock.recv(size), "little")

    def send_uint64(self, data: int) -> None:
        self._send_c_int(data, 8)

    def send_uint32(self, data: int) -> None:
        self._send_c_int(data, 4)

    def recv_uint64(self) -> int:
        return self._recv_c_int(8)

    def recv_uint32(self) -> int:
        return self._recv_c_int(4)

    def send_str(self, data: str) -> None:
        self.send_uint32(len(data))
        self.sock.sendall(data.encode())

    def recv_str(self) -> str:
        size = self.recv_uint32()
        return self.sock.recv(size).decode()

    def send_bytes(self, data: bytes) -> None:
        self.send_uint32(len(data))
        self.sock.sendall(data)

    def recv_bytes(self) -> bytes:
        size = self.recv_uint32()
        return self.sock.recv(size)

    def close(self) -> None:
        self.sock.close()

    def send_vector(self, vector: list[int], size: int = None) -> None:
        if size is None:
            size = len(vector)
        self.send_uint32(size)
        for element in vector:
            self.send_uint64(element)

    def recv_vector(self) -> tuple[list[int], int]:
        size = self.recv_uint32()
        vector = []
        for i in range(size):
            vector.append(self.recv_uint64())
        return vector , size



class Sender(Socket):
    def __init__(self, sock: socket.socket):
        super().__init__(sock)


class Receiver(Socket):
    def __init__(self, sock: socket.socket):
        super().__init__(sock)


