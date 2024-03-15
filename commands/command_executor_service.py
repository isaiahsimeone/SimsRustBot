
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, List

from ipc.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class CommandExecutorService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket
    
    async def execute(self):
        # Get config
        self.config = await self.last_topic_message_or_wait("config")
        # Get socket
        await self.last_topic_message_or_wait("socket_ready")
        self.socket = (await RustSocketManager.get_instance()).socket
        

    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
