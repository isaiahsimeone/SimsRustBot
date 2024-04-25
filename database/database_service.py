
from __future__ import annotations
from typing import TYPE_CHECKING, List

import loguru

from rust_socket.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class DatabaseService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.socket: RustSocketManager
        self.bus = bus
        self.config = {}

    @loguru.logger.catch
    async def execute(self):
        await self.subscribe("player_server_token")
        await self.subscribe("player_fcm_token")
        
        # Get config
        self.config = await self.last_topic_message_or_wait("config")
        # Get socket
        await self.last_topic_message_or_wait("socket_ready")
        self.socket = await RustSocketManager.get_instance()

    
    async def on_message(self, topic: str, message: Message):
        pass
