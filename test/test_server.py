from PyENCRYPTO_utils.connection import listen, Sender
from PyENCRYPTO_utils import *
from CONST import *


# this is server side, play as a OT sender

def InitOTSender(addr, port) -> Sender:
    sock, address = listen(addr, port)
    print(f"connected to {sock.getpeername()}")
    sender = Sender(sock)
    return sender


def main():
    sender = InitOTSender(addr, port)

    vector_size = 10
    vector = [i for i in range(vector_size)]

    sender.send_vector(vector, vector_size)

    sender.close()
    ...


if __name__ == '__main__':
    main()
