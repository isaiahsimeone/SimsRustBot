from queue import Queue, Empty
import threading
from enum import Enum
from util.printer import Printer

class Service(Enum):
    DISCORD = (0, "light_cyan")
    WEBSERVER = (1, "light_magenta")
    RUSTAPI = (2, "light_yellow")

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

    def log(self, service_id, message):
        service_name = service_id.get_name()[0:4]
        colour = service_id.colour;
        Printer.print_info(f"[{service_name}] {message}", colour=colour)
    
    def start(self):
        threading.Thread(target=self.notify_listeners, daemon=True).start()
