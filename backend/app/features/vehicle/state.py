import threading


class State:
    def __init__(self):
        self.frame = None
        self.running = threading.Event()
        self.running.set()
