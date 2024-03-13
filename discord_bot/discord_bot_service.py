
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

import loguru

from ipc.data_models import Test
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

class DiscordBotService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
    
    @loguru.logger.catch
    async def execute(self):
        pass


    
    async def on_message(self, topic: str, message: Message):
        pass
