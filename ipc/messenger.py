from queue import Queue, Empty
import threading
import asyncio
from enum import Enum
from util.printer import Printer
from termcolor import colored
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object

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
        self.message_queue = asyncio.Queue()  # Use asyncio Queue
        self.listeners = {}

    async def send_message(self, service_id, message: Message, target_service_id=None):
        msg_json = message.to_json()
        if target_service_id is not None:
            await self.message_queue.put((service_id, msg_json, target_service_id))
        else:
            await self.message_queue.put((service_id, msg_json, None))
        asyncio.create_task(self.notify_listeners())  # Trigger listener notification

    def subscribe(self, subscribing_service_id, listener_callback):
        self.listeners[subscribing_service_id] = listener_callback

    async def notify_listeners(self):
        try:
            sending_service_id, message, target_service_id = await self.message_queue.get()
            if target_service_id:
                if target_service_id in self.listeners and asyncio.iscoroutinefunction(self.listeners[target_service_id]):
                    asyncio.create_task(self.listeners[target_service_id](message, sending_service_id))
            else:
                for receiving_service_id, listener_callback in self.listeners.items():
                    if receiving_service_id != sending_service_id and asyncio.iscoroutinefunction(listener_callback):
                        asyncio.create_task(listener_callback(message, sending_service_id))
        except asyncio.QueueEmpty:
            pass  # No action needed if queue is empty
    
    async def block_until_subscribed(self, service_id, wait_for):
        self.log(service_id, Service.get_name(service_id) + " is blocking until " + Service.get_name(wait_for) + " is subscribed")
        while wait_for not in self.listeners:
            pass
        self.log(service_id, Service.get_name(service_id) + " is now unblocked")

    def log(self, service_id, message):
        service_name = service_id.get_name()[0:4]
        colour = service_id.colour;
        Printer.print("info", colored(f"[{service_name}] {message}", colour))
    
    def get_config(self):
        return self.config

    # for database
    def add_message(self, user_steam_id, content):
        session = Session()
        user = session.query(User).filter_by(steam_id=user_steam_id).first()
        if not user:
            user = User(steam_id=user_steam_id)
            session.add(user)
            session.commit()

        message = Message(user_id=user.id, content=content)
        
        session.add(message)
        session.commit()
        session.close()