
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, List

import loguru

from ipc.data_models import HeliDespawned, HeliDowned, HeliSpawned, RustTeamChatFull, RustTeamChatMessage
from rust_socket.rust_socket_manager import RustSocketManager
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
        self.socket: RustSocketManager
        
        self.team_info = None
        
        self.all_chat_messages: List[RustTeamChatMessage] = []

    
    @loguru.logger.catch
    async def execute(self: ChatManagerService) -> None:
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = await RustSocketManager.get_instance()
        
        self.team_info = (await self.last_topic_message_or_wait("team_info")).data["team_info"]
        
        await self.publish_initial_team_chat()
        
        # Subscribe to events that should be written to game chat
        # Subscribe after socket is ready, so we can start writing events
        await self.subscribe("heli_spawned")
        await self.subscribe("heli_despawned")
        await self.subscribe("heli_downed")
        await self.subscribe("cargo_spawned")
        await self.subscribe("cargo_despawned")
        await self.subscribe("send_chat_message")
        await self.subscribe("send_player_message") 
        await self.subscribe("team_joined")
        await self.subscribe("team_info")
        await self.subscribe("command_result")
        
        await asyncio.Future()
    
    def can_send_chat(self):
        if not self.team_info:
            return False
        else:
            print("tema info is", self.team_info)
        if not self.team_info.get("leader_steam_id", "") != 0:
            return False
        
    async def publish_initial_team_chat(self):
        initial_team_chat = await self.socket.get_team_chat()
        initial_chat_messages = []
        for message in initial_team_chat:
            initial_chat_messages.append(RustTeamChatMessage(
                steam_id=str(message.steam_id),
                name=message.name,
                message=message.message,
                colour=message.colour,
                time=message.time
            ))
        self.all_chat_messages = initial_chat_messages
        await self.publish("team_chat_full", RustTeamChatFull(messages=initial_chat_messages))
        
        
    async def send_team_message_any(self, *args, **kwargs) -> None:
        if self.can_send_chat():
            self.warning("Dropping team chat message because bot operator not in a team")
            return None
        message = ' '.join(arg for arg in args)
        prefix = kwargs.get("prefix", "[BOT]")
        await self.socket.send_team_message(f"{prefix} {message}")
    
    # Send a message with a specific players socket, if we have one for them
    # or, prefix the message
    async def send_player_team_message(self, chat: dict[str, Any]):
        if self.can_send_chat():
            self.warning("Dropping team chat message because bot operator not in a team")
            return None
        self.debug("sending player team chat message")
        send_with = self.socket.leader_socket.steam_id
        message = ""
        # Does the socket have a token for the sending steam id? If so, we send with that
        if self.socket.has_token_for_steam_id(chat["steam_id"]):
            self.debug("we have a token for this dude")
            send_with = int(chat["steam_id"])
        else:
            message += f"[{chat['steam_id']} "
        
        message += chat["message"]
        
        await self.socket.send_team_message(message, steam_id=send_with)
        await self.publish("team_message", RustTeamChatMessage(steam_id=chat["steam_id"], name=chat["name"],
                                                               message=chat["message"], colour=chat["colour"], time=chat["time"]))
        

    async def send_heli_message(self, message: Message) -> None:
        model: dict[str, Any] = message.data
        match message.type:
            case "HeliDowned":
                self.debug("heli downed")
                await self.send_team_message_any("Heli was downed TODO: what grid?")
            case "HeliSpawned":
                self.debug("heli spawned")
                await self.send_team_message_any(f"Heli just spawned! It will enter the map from the {model['cardinal_bearing']}")
            case "HeliDespawned":
                self.debug("heli despawned")
                await self.send_team_message_any("Heli has despawned")
            case _:
                self.error(f"I don't know how to send {message.type} in send_heli_message()")
    
    async def send_cargo_message(self, message: Message) -> None:
        
        model: dict[str, Any] = message.data
        match message.type:
            case "CargoSpawned":
                self.debug("cargo spawned")
                await self.send_team_message_any(f"CargoShip just spawned! It will enter the map from the {model['cardinal_bearing']}")
            case "CargoDespawned":
                self.debug("cargo despawned")
                await self.send_team_message_any(f"CargoShip has despawned")
            case _:
                self.error(f"I don't know how to send {message.type} in send_cargo_message()")
    
    @loguru.logger.catch
    async def on_message(self, topic: str, message: Message) -> None:
        match topic:
            case "send_chat_message":
                prefix = message.data["prefix"]
                msg = message.data["message"]
                await self.send_team_message_any(msg, prefix=f"[{prefix}]")
            case "send_player_message":
                await self.send_player_team_message(message.data) # type: ignore
            case "heli_spawned" | "heli_despawned" | "heli_downed":
                await self.send_heli_message(message)
            case "cargo_spawned" | "cargo_despawned":
                await self.send_cargo_message(message)
            case "team_joined":
                await self.publish_initial_team_chat()
            case "team_info":
                self.team_info = message.data
            case "team_message":
                chat = message.data
                self.all_chat_messages.append(RustTeamChatMessage(steam_id=chat["steam_id"],
                                                                  name=chat["name"],
                                                                  message=chat["message"],
                                                                  colour=chat["colour"],
                                                                  time=chat["time"]))
                await self.publish("team_chat_full", RustTeamChatFull(messages=self.all_chat_messages))
            case "command_result":
                await self.send_team_message_any(message.data["message"])
            case _:
                self.error(f"I received a Message under topic '{topic}', but I have no implementation to handle it")
        self.debug(f"Got message ({topic})")
