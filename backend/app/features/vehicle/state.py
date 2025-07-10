import queue
import threading


class State:
    def __init__(self, maxsize=100):
        self.queue = queue.Queue(maxsize=maxsize)
        self.running = threading.Event()
        self.running.set()
