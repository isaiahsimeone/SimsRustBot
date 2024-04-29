
from __future__ import annotations
from typing import TYPE_CHECKING, List

import loguru

from ipc.data_models import RustTeamChatMessage
from rust_socket.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    from rustplus import ChatEvent, TeamEvent, EntityEvent, ProtobufEvent

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

class EventListenerService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        
    
    @loguru.logger.catch
    async def execute(self):
        # Get config
        self.config = await self.last_topic_message_or_wait("config")
        
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = await RustSocketManager.get_instance()
        
        self.socket.chat_event(self.chat_event_handler)
        self.socket.team_event(self.team_event_handler)
        self.socket.protobuf_received(self.protobuf_received_handler)
        
        
    async def team_event_handler(self, event: TeamEvent):
        team_info = event.team_info

        self.debug("team_event", event)
        
    async def chat_event_handler(self, event: ChatEvent):
        model = RustTeamChatMessage(steam_id=str(event.message.steam_id),
                                    name=event.message.name,
                                    message=event.message.message,
                                    colour=event.message.colour,
                                    time=event.message.time)
        
        await self.publish("team_message", model)
    
    def protobuf_received_handler(self, event: ProtobufEvent):
        pass
        

    
    async def on_message(self, topic: str, message: Message):
        self.debug(f"Bus message ({topic}):", message)
