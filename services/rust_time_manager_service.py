
from __future__ import annotations
from typing import TYPE_CHECKING, List

import loguru
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class RustTimeManagerService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
    
    @loguru.logger.catch
    async def execute(self):
        # Get config
        self.config = await self.last_topic_message_or_wait("config")
        
        # Connect to the rust server
        

    
    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
