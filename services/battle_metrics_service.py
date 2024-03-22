
from __future__ import annotations
from typing import TYPE_CHECKING

import loguru

from ipc.rust_socket_manager import RustSocketManager
import util
from util.tools import Tools
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class BattleMetricsService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket
        
        self.battlemetrics_api_key = ""
    
    @loguru.logger.catch
    async def execute(self: BattleMetricsService) -> None:
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = (await RustSocketManager.get_instance()).socket
        # Set map polling frequency
        #self.battlemetrics_api_key = self.config["BattleMetricsService"]["api_key"]
        # Get server info - RustPlusAPIService publishes this on startup to save tokens
        self.server_info = (await self.last_topic_message_or_wait("server_info")).data["server_info"]
        
        if not self.battlemetrics_api_key:
            self.warning("No API key specified. This service will not be started.")
            return None
    
    async def on_message(self: BattleMetricsService, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
