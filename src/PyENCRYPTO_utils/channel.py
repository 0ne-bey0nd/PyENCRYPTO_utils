# private:
# 	uint8_t m_bChannelID;
# 	RcvThread* m_cRcver;
# 	SndThread* m_cSnder;
# 	std::unique_ptr<CEvent> m_eRcved;
# 	std::unique_ptr<CEvent> m_eFin;
# 	bool m_bSndAlive;
# 	bool m_bRcvAlive;
# 	std::queue<rcv_ctx*>* m_qRcvedBlocks;
# 	std::mutex& m_qRcvedBlocks_mutex_;

import socket
import threading
import queue
from .sender_thread import SenderThread
from .receiver_thread import ReceiverThread, RcvContext


class Channel:
    def __init__(self, channel_id: int, receiver_thread: ReceiverThread, sender_thread: SenderThread):
        self.channel_id = channel_id
        self.receiver_thread = receiver_thread
        self.sender_thread = sender_thread
        self.rcv_event = threading.Event()
        self.fin_event = threading.Event()
        self.sender_alive = True
        self.receiver_alive = True
        self.received_blocks = receiver_thread.add_listener(channel_id, self.rcv_event,
                                                            self.fin_event)  # type: queue.Queue[RcvContext]
        self.received_blocks_mutex = threading.Lock()

        assert receiver_thread.get_lock() == sender_thread.get_lock()

    def send(self, buf: bytes):
        assert self.sender_alive
        self.sender_thread.add_snd_task(self.channel_id, len(buf), buf)

    def blocking_send(self, event_caller: threading.Event, buf: bytes):
        assert self.sender_alive
        self.sender_thread.add_event_snd_task(event_caller, self.channel_id, len(buf), buf)
        event_caller.wait()

    def send_id_len(self, buf: bytes, id: int, length: int):
        assert self.sender_alive
        self.sender_thread.add_snd_task_start_len(self.channel_id, len(buf), buf, id, length)

    def blocking_receive_id_len(self) -> tuple[bytes, int, int]:
        buf = self.blocking_receive()
        id = int.from_bytes(buf[:8], "little")
        length = int.from_bytes(buf[8:16], "little")
        return buf[16:], id, length

    def queue_empty(self) -> bool:
        with self.received_blocks_mutex:
            return self.received_blocks.empty()

    def blocking_receive(self) -> bytes:
        assert self.receiver_alive
        while self.queue_empty():
            self.rcv_event.wait()
        with self.received_blocks_mutex:
            ret = self.received_blocks.get()
            ret_block = ret.buf
            del ret
        return ret_block

    def blocking_receive_into(self, rcvbuf: bytearray, rcvsize: int):
        assert self.receiver_alive
        while self.queue_empty():
            self.rcv_event.wait()
        with self.received_blocks_mutex:
            ret = self.received_blocks.get()
            ret_block = ret.buf
            rcved_this_call = ret.rcvbytes
            if rcved_this_call == rcvsize:
                del ret
            elif rcvsize < rcved_this_call:
                ret.rcvbytes -= rcvsize
                newbuf = ret_block[rcvsize:]
                ret_block = newbuf
                rcved_this_call = rcvsize
            else:
                del ret
                new_rcvbuf_start = rcvbuf[rcved_this_call:]
                new_rcvsize = rcvsize - rcved_this_call
                self.blocking_receive_into(new_rcvbuf_start, new_rcvsize)
            rcvbuf[:rcved_this_call] = ret_block
            del ret_block

    def is_alive(self) -> bool:
        return not (self.queue_empty() and self.fin_event.is_set())

    def data_available(self) -> bool:
        return not self.queue_empty()

    def signal_end(self):
        self.sender_thread.signal_end(self.channel_id)
        self.sender_alive = False

    def wait_for_fin(self):
        self.fin_event.wait()
        self.receiver_alive = False

    def synchronize_end(self):
        if self.sender_alive:
            self.signal_end()
        if self.receiver_alive:
            self.receiver_thread.flush_queue(self.channel_id)
        if self.receiver_alive:
            self.wait_for_fin()
