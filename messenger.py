from queue import Queue, Empty
import threading

class Messenger:
    def __init__(self):
        self.message_queue = Queue()
        self.listeners = []
        pass

    

