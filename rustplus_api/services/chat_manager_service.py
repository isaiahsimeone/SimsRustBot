
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any

import loguru

from ipc.data_models import RustHeliDespawned, RustHeliDowned, RustHeliSpawned
from ipc.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket

# Sends shit to the chat

class ChatManagerService(BusSubscriber, Loggable):
    def __init__(self: ChatManagerService, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket

    
    @loguru.logger.catch
    async def execute(self: ChatManagerService) -> None:
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = (await RustSocketManager.get_instance()).socket
        # Subscribe to events that should be written to game chat
        await self.subscribe("heli")
        await self.subscribe("cargo")
        
        await asyncio.Future()
        
    async def send_team_message(self, *args) -> None:
        message = ' '.join(arg for arg in args)
        await self.socket.send_team_message(message)

    async def send_heli_message(self, message: Message) -> None:
        model: dict[str, Any] = message.data
        match message.type:
            case "RustHeliDowned":
                await self.send_team_message("Heli was DOWNED ")
            case "RustHeliSpawned":
                await self.send_team_message(f"Heli just spawned! It will enter the map from the {model['cardinal_bearing']}")
            case "RustHeliDespawned":
                await self.send_team_message("Heli has despawned")
            case _:
                self.error(f"I don't know how to send {message.type} in send_heli_message()")
    
    async def send_cargo_message(self, message: Message) -> None:
        pass
    
    async def on_message(self, topic: str, message: Message) -> None:
        match topic:
            case "heli":
                await self.send_heli_message(message)
            case "cargo":
                await self.send_cargo_message(message)
            case _:
                self.error(f"I received a Message under topic '{topic}', but I have no implementation to handle it")
        self.debug(f"Got message ({topic})")
