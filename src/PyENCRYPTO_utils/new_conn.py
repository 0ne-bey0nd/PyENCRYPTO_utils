import argparse
import socket
import threading

from PyENCRYPTO_utils.sender_thread import SenderThread
from PyENCRYPTO_utils.receiver_thread import ReceiverThread
from PyENCRYPTO_utils.connection import Listen, Connect
from PyENCRYPTO_utils.channel import Channel
from PyENCRYPTO_utils.constants import ADMIN_CHANNEL

SEVER = 0
CLIENT = 1


class CommunicationContext:
    def __init__(self):
        self.rcv_std: ReceiverThread = None
        self.rcv_inv: ReceiverThread = None
        self.snd_std: SenderThread = None
        self.snd_inv: SenderThread = None


def listen(address: str, port: int, role: int) -> list[socket.socket]:
    temp_socks = [[None, None], [None, None]]
    success = Listen(address, port, temp_socks, len(temp_socks), role)
    return temp_socks[CLIENT]


def connect(address: str, port: int, role: int) -> list[socket.socket]:
    temp_socks = [None, None]
    success = Connect(address, port, temp_socks, role)
    return temp_socks


def establish_connection(address: str, port: int, role: int) -> CommunicationContext:
    success = False
    if role == SEVER:
        socks = listen(address, port, role)
    else:
        socks = connect(address, port, role)

    glock = threading.Lock()
    communication_context = CommunicationContext()
    communication_context.snd_std = SenderThread(socks[0], glock)
    communication_context.rcv_std = ReceiverThread(socks[0], glock)
    communication_context.snd_inv = SenderThread(socks[1], glock)
    communication_context.rcv_inv = ReceiverThread(socks[1], glock)

    communication_context.snd_std.start()
    communication_context.snd_inv.start()
    communication_context.rcv_std.start()
    communication_context.rcv_inv.start()

    return communication_context
    ...


def main():
    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description='...')
    # 添加位置参数
    parser.add_argument('--role', choices=[0, 1], type=int, required=True, help='...')
    parser.add_argument('--port', type=int, required=True, help='...')

    # 解析命令行参数
    args = parser.parse_args()

    address = "localhost"
    role = args.role
    port = args.port

    print(f"role={role}, port={port}")

    communication_context = establish_connection(address, port, role)

    channel = Channel(0, communication_context.rcv_std, communication_context.snd_std)

    # if role == SEVER:
    #     print("Server sent message to client")
    #     channel.send(b"Hello, client!")
    #     print("Server received message: ", channel.blocking_receive())
    # else:
    #     print(f"Client received message: {channel.blocking_receive()}")
    #     print("Client sent message to server")
    #     channel.send(b"Hello, server!")

    ...
    channel.synchronize_end()
    print("begin to close")
    communication_context.snd_std.kill_task()
    communication_context.snd_inv.kill_task()
    print("end to close")


if __name__ == '__main__':
    main()
    ...
