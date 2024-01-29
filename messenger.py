from queue import Queue, Empty
import sys
import threading
from enum import Enum
from termcolor import colored

class Service(Enum):
    DISCORD = (0, "light_cyan")
    WEBSERVER = (1, "light_magenta")
    RUSTAPI = (2, "light_yellow")

    def __init__(self, value, color):
        self._value_ = value
        self.color = color

    def get_name(self):
        return self.name

class Messenger:
    def __init__(self):
        self.message_queue = Queue()
        self.listeners = {}

    def send_message(self, service_id, message):
        self.message_queue.put((service_id, message))
        
    def subscribe(self, subscribing_service_id, listener_callback):
        self.listeners[subscribing_service_id] = listener_callback

    def notify_listeners(self):
        while True:
            try:
                sending_service_id, message = self.message_queue.get()
                for receiving_service_id, listener_callback in self.listeners.items():
                    if receiving_service_id != sending_service_id:
                        listener_callback(message)
            except Empty:
                continue

    def print(self, service_id, *args, file=sys.stdout, sep=' ', end='\n', flush=False):
        service_name = service_id.get_name()[0:4]
        color = service_id.color
        output = sep.join(map(str, args))
        file.write(colored(f"[{service_name}] {output}", color) + end)
        if flush:
            file.flush()
    
    def start(self):
        threading.Thread(target=self.notify_listeners, daemon=True).start()
