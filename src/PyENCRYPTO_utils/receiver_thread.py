import threading
import queue
from .constants import MAX_NUM_COMM_CHANNELS, ADMIN_CHANNEL


class RcvContext:
    def __init__(self, buf: bytes, rcvbytes: int):
        self.buf = buf
        self.rcvbytes = rcvbytes


class RcvTask:
    def __init__(self):
        self.rcv_buf = queue.Queue()  # type: queue.Queue[RcvContext]
        self.rcv_buf_mutex = threading.Lock()
        self.rcv_event = threading.Event()
        self.fin_event = threading.Event()
        self.inuse = False
        self.forward_notify_fin = False


class ReceiverThread(threading.Thread):

    def __init__(self, sock, glock: threading.Lock):
        threading.Thread.__init__(self)
        self.receiver_lock = glock
        self.sock = sock
        self.listeners: list[RcvTask] = [RcvTask() for _ in range(MAX_NUM_COMM_CHANNELS)]
        self.listeners[ADMIN_CHANNEL].inuse = True

    def get_lock(self) -> threading.Lock:
        return self.receiver_lock

    def flush_queue(self, channelid: int):
        with self.listeners[channelid].rcv_buf_mutex:
            while not self.listeners[channelid].rcv_buf.empty():
                tmp = self.listeners[channelid].rcv_buf.get()
                del tmp

    def remove_listener(self, channelid: int):
        with self.receiver_lock:
            if self.listeners[channelid].inuse:
                self.listeners[channelid].fin_event.set()
                self.listeners[channelid].inuse = False
            else:
                self.listeners[channelid].forward_notify_fin = True

    def add_listener(self, channelid: int, rcv_event: threading.Event, fin_event: threading.Event) -> queue.Queue[
        RcvContext]:
        with self.receiver_lock:
            if self.listeners[channelid].inuse or channelid == ADMIN_CHANNEL:
                print(f"A listener has already been registered on channel {channelid}")
                assert not self.listeners[channelid].inuse
                assert channelid != ADMIN_CHANNEL
            self.listeners[channelid].rcv_event = rcv_event
            self.listeners[channelid].fin_event = fin_event
            self.listeners[channelid].inuse = True
            if self.listeners[channelid].forward_notify_fin:
                self.listeners[channelid].forward_notify_fin = False
                self.remove_listener(channelid)
            return self.listeners[channelid].rcv_buf

    def run(self) -> None:
        while True:
            # std::cout << "Starting to receive data" << std::endl;
            print("Starting to receive data")
            rcv_len = 0

            channelid_in_bytes = self.sock.recv(1)
            rcvbytelen_in_bytes = self.sock.recv(8)

            rcv_len += 1
            rcv_len += 8

            # print(rcvbytelen_in_bytes)

            channelid = int.from_bytes(channelid_in_bytes, "little")
            rcvbytelen = int.from_bytes(rcvbytelen_in_bytes, "little")

            if rcv_len > 0:
                # #ifdef DEBUG_RECEIVE_THREAD
                # std::cout << "Received value on channel " << (uint32_t) channelid << " with " << rcvbytelen <<
                #         " bytes length (" << rcv_len << ")" << std::endl;
                # #endif

                print(f"Received value on channel {channelid} with {rcvbytelen} bytes length ({rcv_len})")

                if channelid == ADMIN_CHANNEL:
                    tmprcvbuf = self.sock.recv(rcvbytelen)
                    print(f"Received on admin channel, begin to stop the receiver thread")
                    return

                if rcvbytelen == 0:
                    self.remove_listener(channelid)

                else:
                    rcv_buf = RcvContext(self.sock.recv(rcvbytelen), rcvbytelen)
                    with self.receiver_lock:
                        with self.listeners[channelid].rcv_buf_mutex:
                            self.listeners[channelid].rcv_buf.put(rcv_buf)
                        cond = self.listeners[channelid].inuse
                    if cond:
                        print(f"Signalling event on channel {channelid}")
                        self.listeners[channelid].rcv_event.set()

            else:
                # We received 0 bytes, probably due to some major error. Just return.
                return
