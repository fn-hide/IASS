import queue
import threading


class State:
    def __init__(self):
        self.queue = queue.Queue(maxsize=100)
        self.running = threading.Event()
        self.running.set()


state = State()
