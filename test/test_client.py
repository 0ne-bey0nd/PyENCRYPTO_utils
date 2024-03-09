from PyENCRYPTO_utils.connection import connect,Receiver
from PyENCRYPTO_utils import *

from CONST import *


# this is client side, play as a OT receiver
def InitOTReceiver(addr, port) -> Receiver:
    sock = connect(addr, port)
    print(f"connected to {sock.getpeername()}")
    receiver = Receiver(sock)
    return receiver

def main():
    receiver = InitOTReceiver(addr, port)
    vector, vector_size = receiver.recv_vector()
    print(vector)

    receiver.close()
    ...


if __name__ == '__main__':
    main()
