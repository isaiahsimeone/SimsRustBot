
from __future__ import annotations
import asyncio
import copy
import json
from typing import TYPE_CHECKING, List

import loguru

from ipc.data_models import Empty
from ipc.rust_socket_manager import RustSocketManager

if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class RustPlusAPIService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket
    
    @loguru.logger.catch
    async def execute(self):
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        # Connect to the rust server
        await self.connect_to_server()
        
        # The socket is ready for all services to use
        await self.publish("socket_ready", Message(Empty()))
        
    async def connect_to_server(self):
        ip = self.config["server_details"]["ip"]
        port = self.config["server_details"]["port"]
        playerId = self.config["server_details"]["playerId"]
        playerToken = self.config["server_details"]["playerToken"]

        rust_socket_manager = await RustSocketManager.get_instance()

        await rust_socket_manager.initialise_socket(ip, port, playerId, playerToken)

        self.info(f"Connected to {ip}:{port}!")
        
        print(await rust_socket_manager.socket.get_time())
    
    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
