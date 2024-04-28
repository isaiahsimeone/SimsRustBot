
from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

import loguru

from ipc.data_models import Empty, PlayerServerToken, RustServerInfo
from rust_socket.client_rust_socket import ClientRustSocket
from rust_socket.rust_socket_manager import RustSocketManager

if TYPE_CHECKING:
    from rustplus import RustSocket

    from ipc.message_bus import MessageBus

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from log.loggable import Loggable

from rustplus.api.structures.rust_info import RustInfo

class RustPlusAPIService(BusSubscriber, Loggable):
    def __init__(self: RustPlusAPIService, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocketManager
        
        self.connected_rust_server_ip: str
        
        self.server_info: RustInfo
    
    @loguru.logger.catch
    async def execute(self: RustPlusAPIService) -> None:
        """The main point of execution for the service.

        :param self: This instance
        :type self: :class:`RustPlusAPIService <rustplus_api.rust_plus_api_server.RustPlusAPIService>`
        """
        await self.subscribe("player_server_token")
        await self.subscribe("player_fcm_token")
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        # Connect to the rust server
        await self.connect_to_server()
        
        # Fetch and publish server info, the majority of services will probably use it
        self.server_info = await self.socket.get_info()
        await self.publish("server_info", RustServerInfo(server_info=self.server_info))
        
        # The database service will publish this on startup. Wait for it, and register those sockets
        stored_player_tokens = (await self.last_topic_message_or_wait("database_player_server_tokens")).data["tokens"]
        for player_token in stored_player_tokens:
            await self.register_player_server_token(player_token)
        
        # The socket is ready for services to use
        await self.publish("socket_ready", Empty())
        
        await asyncio.Future()
        
    async def connect_to_server(self: RustPlusAPIService) -> None:
        """Connect to the rust server. Details are taken from the config, 
        provided by the :class:ConfigServiceManager <`config.config_server_manager.ConfigServiceManager`>.

        :param self: This instance
        :type self: :class:`RustPlusAPIService <rustplus_api.rust_plus_api_server.RustPlusAPIService>`
        """
        self.connected_rust_server_ip = self.config["server_details"]["ip"]
        port = self.config["server_details"]["port"]
        playerId = self.config["server_details"]["playerId"]
        playerToken = self.config["server_details"]["playerToken"]

        self.socket = await RustSocketManager.get_instance()
        await self.socket.initialise_socket_leader(self.connected_rust_server_ip, port, playerId, playerToken)
        
        self.info(f"Connected to {self.connected_rust_server_ip}:{port}!")
    
    @loguru.logger.catch
    async def on_message(self: RustPlusAPIService, topic: str, message: Message) -> None:
        """Receive a message, under a subscribed topic, from the bus.

        :param self: This instance
        :type self: :class:`RustPlusAPIService <rustplus_api.rust_plus_api_server.RustPlusAPIService>`
        :param topic: The topic of the message being received
        :type topic: str
        :param message: The message being received
        :type message: :class:`Message<ipc.message.Message>`
        """
        match topic:
            case "player_server_token":
                self.info("GOT PLAYER_SERVER_TOKEN")
                token = message.data
                await self.register_player_server_token(token)
            case "player_fcm_token":
                pass
            case _:
                self.error(f"Encountered topic {topic} that I have no case for")


    async def register_player_server_token(self: RustPlusAPIService, token_data: dict[str, Any]) -> None:
        token = PlayerServerToken.from_dict(token_data)
        self.debug("creating client socket", token.ip, token.port, token.steam_id, token.playerToken)
        
        if self.socket.leader_socket.steam_id == token.steam_id:
            self.warning("The bot operator tried to overwrite their own FCM credentials. Ignoring")
            return None
        
        if self.connected_rust_server_ip != token.ip:
            self.error(f"A server token for {token.steam_id} is for ip {token.ip}. But")
            self.error(f"the bot operator is connected to {self.connected_rust_server_ip}")
        
        self.socket.create_socket_thread(token.ip, token.port, token.steam_id, token.playerToken)
        
        self.debug("created client socket")