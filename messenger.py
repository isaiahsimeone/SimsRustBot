from queue import Queue, Empty
import threading
from enum import Enum
from util.printer import Printer
from termcolor import colored

class Service(Enum):
    DISCORD = (1, "light_cyan")
    WEBSERVER = (2, "light_magenta")
    RUSTAPI = (3, "light_yellow")

    def __init__(self, value, colour):
        self._value_ = value
        self.colour = colour

    def get_name(self):
        return self.name

class Messenger:
    def __init__(self, config):
        self.config = config
        self.message_queue = Queue()
        self.listeners = {}

    def send_message(self, service_id, message, target_service_id=None):
        # If target_service_id is specified, send only to that listener.
        # Otherwise, send to all listeners except the sender.
        if target_service_id is not None:
            self.message_queue.put((service_id, message, target_service_id))
        else:
            self.message_queue.put((service_id, message, None))
        self.notify_listeners()

    def subscribe(self, subscribing_service_id, listener_callback):
        self.listeners[subscribing_service_id] = listener_callback

    def notify_listeners(self):
        while True:
            try:
                sending_service_id, message, target_service_id = self.message_queue.get()
                if target_service_id:
                    # Send to specific listener
                    if target_service_id in self.listeners:
                        self.listeners[target_service_id](message, sending_service_id)
                else:
                    # Broadcast to all listeners except the sender
                    for receiving_service_id, listener_callback in self.listeners.items():
                        if receiving_service_id != sending_service_id:
                            listener_callback(message, sending_service_id)
            except Empty:
                continue

    def log(self, service_id, message):
        service_name = service_id.get_name()[0:4]
        colour = service_id.colour;
        Printer.print("info", colored(f"[{service_name}] {message}", colour))
    
    def get_config(self):
        return self.config
