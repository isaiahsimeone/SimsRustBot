from __future__ import annotations
from base64 import b64encode
from io import BytesIO
from typing import TYPE_CHECKING
from ipc.data_models import RustMapMonuments, RustServerInfo, RustServerMap, RustTeamChatFull, RustTeamInfo
if TYPE_CHECKING:
    from rust_plus_api import RustPlusAPI

from ipc.message import MessageType as MT

from ipc.message import Message
from PIL import Image
import io
from util.loggable import Loggable

class MessageExecutor(Loggable):
    def __init__(self, rust_api: RustPlusAPI):
        self.api = rust_api
        self.socket = self.api.get_socket()
        super().__init__(rust_api.log)
        
        self.raw_map_data = None
        self.server_info = None
        self.map_sz = 0
                    
    def get_message_type(self, value):
        for member in MT:
            if member.value == value:
                return member
        return None
    
    async def execute_message(self, msg, sender):
        msg_type = self.get_message_type(msg.get("type"))
        data = msg.get("data")
        match msg_type:
            case MT.REQUEST_RUST_SERVER_MAP:
                await self.send_server_map_image(sender)
            case MT.REQUEST_RUST_MAP_MONUMENTS:
                await self.send_server_map_monuments(sender)
            case MT.REQUEST_RUST_SERVER_INFO:
                await self.send_server_info(sender)
            case MT.REQUEST_RUST_TEAM_INFO:
                await self.send_team_info(sender)
            case MT.REQUEST_RUST_TEAM_CHAT_INIT:
                await self.send_team_chat_init(sender)
            case MT.REQUEST_SEND_TEAM_MESSAGE:
                await self.send_rust_message(sender, data['message'], data['name']) # last arg is steam name
            case MT.REQUEST_ITEM_COUNT:
                await self.send_item_count(sender, data)
            case _:
                self.log("MessageExecutor received an unknown message: " + str(msg), type="error")
                
    async def send_rust_message(self, sending_service, message, steam_name):
        await self.api.send_game_message(message, steam_name)

    async def send_server_map_image(self, sender):
        # Saves API tokens
        if not self.raw_map_data:
            self.raw_map_data = await self.socket.get_raw_map_data()
        
        img_data = self.raw_map_data.jpg_image
        width = self.raw_map_data.width
        height = self.raw_map_data.height
       
        encoded = b64encode(img_data).decode("UTF-8")
       
        map_data = RustServerMap(width=width, height=height, pixels=encoded)
        message = Message(MT.RUST_SERVER_MAP, map_data)
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_server_map_monuments(self, sender):
        # Saves API tokens
        if not self.raw_map_data:
            self.raw_map_data = await self.socket.get_raw_map_data()
        
        background = self.raw_map_data.background
        
        data = RustMapMonuments(monuments=self.raw_map_data.monuments, background=background)
        message = Message(MT.RUST_MAP_MONUMENTS, data)
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_server_info(self, sender):
        if not self.server_info:
            self.server_info = await self.socket.get_info()
            
        server_info = self.server_info
        
        data = RustServerInfo(
            url = server_info.url,
            name = server_info.name,
            size = server_info.size,
            map = server_info.map,
            players = server_info.players,
            max_players = server_info.max_players,
            queued_players = server_info.queued_players,
            seed = server_info.seed,
            wipe_time = server_info.wipe_time,
            header_image = server_info.header_image,
            logo_image = server_info.logo_image     
        )
        
        message = Message(MT.RUST_SERVER_INFO, data)
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_info(self, sender):
        team_info = await self.socket.get_team_info()
        
        data = RustTeamInfo(
            leader_steam_id=team_info.leader_steam_id,
            members=team_info.members,
            map_notes=team_info.map_notes,
            leader_map_notes=team_info.leader_map_notes
        )
        
        message = Message(MT.RUST_TEAM_INFO, data)
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_chat_init(self, sender):
        initial_team_chat = None
        try:
            initial_team_chat = await self.socket.get_team_chat()
        except:
            return # Not in a team. 
        data = RustTeamChatFull(chats=initial_team_chat)
        message = Message(MT.RUST_TEAM_CHAT_INIT, data)
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_item_count(self, sender, data):
        
        #message = Message(MessageType.RUST_TEAM_CHAT_INIT, {"count": item_count})
        #await self.api.send_message(message, target_service_id=sender)
        pass