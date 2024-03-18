import threading
import queue
from .constants import MAX_NUM_COMM_CHANNELS, ADMIN_CHANNEL


class SndTask:
    def __init__(self):
        self.channel_id = 0
        self.snd_buf = b""  # type: bytes
        self.event_caller = threading.Event()


class SenderThread(threading.Thread):
    def __init__(self, sock, glock: threading.Lock):
        threading.Thread.__init__(self)
        self.sender_lock = glock
        self.sock = sock
        self.send = threading.Event()

        self.send_task_queue = queue.Queue()

    def kill_task(self):
        task = SndTask()
        task.channel_id = ADMIN_CHANNEL
        task.snd_buf = b'\x00'
        self.push_task(task)
        print(f"Killing channel {task.channel_id}")
        self.join()

    def get_lock(self) -> threading.Lock:
        return self.sender_lock

    def push_task(self, task: SndTask):
        with self.sender_lock:
            self.send_task_queue.put(task)
        self.send.set()

    def add_event_snd_task_start_len(self, event_caller: threading.Event, channel_id: int, snd_bytes: int,
                                     sndbuf: bytes, startid: int, len: int):
        assert channel_id != ADMIN_CHANNEL
        task = SndTask()
        task.channel_id = channel_id
        task.event_caller = event_caller
        bytelen = snd_bytes + 2 * 8
        task.snd_buf += (startid.to_bytes(8, "little"))
        task.snd_buf += (len.to_bytes(8, "little"))
        task.snd_buf += (sndbuf)
        self.push_task(task)

    def add_snd_task_start_len(self, channel_id: int, snd_bytes: int, sndbuf: bytes, startid: int, len: int):
        self.add_event_snd_task_start_len(None, channel_id, snd_bytes, sndbuf, startid, len)

    def add_event_snd_task(self, event_caller: threading.Event, channel_id: int, snd_bytes: int, sndbuf: bytes):
        assert channel_id != ADMIN_CHANNEL
        task = SndTask()
        task.channel_id = channel_id
        task.event_caller = event_caller
        task.snd_buf = sndbuf

        self.push_task(task)

    def add_snd_task(self, channel_id: int, snd_bytes: int, sndbuf: bytes):
        self.add_event_snd_task(None, channel_id, snd_bytes, sndbuf)

    def signal_end(self, channel_id: int):
        self.add_snd_task(channel_id, 0, b'')
        print(f"Signalling end on channel {channel_id}")

    def run(self):
        run = True
        empty = True
        while run:
            with self.sender_lock:
                empty = self.send_task_queue.empty()
            if empty:
                self.send.wait()
            with self.sender_lock:
                iters = self.send_task_queue.qsize()
            while iters and run:
                with self.sender_lock:
                    task = self.send_task_queue.get()
                channel_id = task.channel_id
                self.sock.send(channel_id.to_bytes(1, "little"))
                bytelen = len(task.snd_buf)
                self.sock.send(bytelen.to_bytes(8, "little"))
                if bytelen > 0:
                    self.sock.send(task.snd_buf)
                if channel_id == ADMIN_CHANNEL:
                    run = False
                if task.event_caller is not None:
                    task.event_caller.set()
                iters -= 1
        print("Sender thread terminated")
        return
