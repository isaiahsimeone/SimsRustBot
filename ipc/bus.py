from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config.config_manager import ConfigManager
    from database.database import Database

import asyncio
from enum import Enum
from util.printer import Printer
from termcolor import colored
from ipc.message import Message

class Service(Enum):
    DISCORD = (1, "light_cyan")
    WEBSERVER = (2, "light_magenta")
    RUSTAPI = (3, "light_yellow")

    def __init__(self, value, colour):
        self._value_ = value
        self.colour = colour

    def get_name(self):
        return self.name

class BUS:
    def __init__(self, config: ConfigManager, database: Database):
        self.config = config
        self.message_queue = asyncio.Queue()  # Use asyncio Queue
        self.listeners = {}
        self.database = database

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
        if wait_for in self.listeners:
            return 
        self.log(service_id, Service.get_name(service_id) + " is blocked until " + Service.get_name(wait_for) + " is subscribed")
        while wait_for not in self.listeners:
            pass
        self.log(service_id, Service.get_name(service_id) + " is now unblocked")

    def log(self, service_id, message, type="info"):
        service_name = service_id.get_name()[0:4]
        colour = service_id.colour;
        Printer.print(type, colored(f"[{service_name}] {message}", colour))
    
    def get_config(self):
        return self.config


    def db_insert(self, table, data):
        self.database.insert(table, data)
        
    def db_query(self, what, table, where):
        return self.database.query(what, table, where)
    
    def db_delete_from(self, table, where):
        return self.database.delete_from(table, where)


   
        
    