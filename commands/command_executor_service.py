
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

class CommandExecutorService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
    
    async def execute(self):
        pass

    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
