from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rust_plus_api import RustPlusAPI

from ipc.message import MessageType as MT

from ipc.message import Message, MessageType

from util.loggable import Loggable

class MessageExecutor(Loggable):
    def __init__(self, rust_api: RustPlusAPI):
        self.api = rust_api
        self.socket = self.api.get_socket()
        super().__init__(rust_api.log)
                    
    def get_message_type(self, value):
        for member in MT:
            if member.value == value:
                return member
        return None
    
    async def execute_message(self, msg, sender):
        msg_type = self.get_message_type(msg.get("type"))
        
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
            case MT.SEND_TEAM_MESSAGE:
                await self.send_rust_message(sender, msg["data"]["message"], msg["data"]["sender"]) # last arg is steam name
            case MT.REQUEST_ITEM_COUNT:
                await self.send_item_count(sender, msg)
            case _:
                self.log("MessageExecutor received an unknown message: " + str(msg), type="error")
                
    async def send_rust_message(self, sending_service, message, steam_name):
        await self.api.send_game_message(message, steam_name)

    async def send_server_map_image(self, sender):
        map_image = await self.socket.get_map()
    
        pixel_data = list(map_image.getdata())

        server_map = {
            'width': map_image.width,
            'height': map_image.height,
            'pixels': pixel_data
        }
        
        message = Message(MessageType.RUST_SERVER_MAP, {"data": server_map})
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_server_map_monuments(self, sender):
        server_monuments = await self.socket.get_raw_map_data()
        message = Message(MessageType.RUST_MAP_MONUMENTS, {"data": server_monuments})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_server_info(self, sender):
        server_info = await self.socket.get_info()
        message = Message(MessageType.RUST_SERVER_INFO, {"data": server_info})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_info(self, sender):
        team_info = await self.socket.get_team_info()
        message = Message(MessageType.RUST_TEAM_INFO, {"data": team_info})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_chat_init(self, sender):
        initial_team_chat = None
        try:
            initial_team_chat = await self.socket.get_team_chat()
        except:
            pass # Not in a team. None
        message = Message(MessageType.RUST_TEAM_CHAT_INIT, {"data": initial_team_chat})
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_item_count(self, sender, data):
        
        #message = Message(MessageType.RUST_TEAM_CHAT_INIT, {"count": item_count})
        #await self.api.send_message(message, target_service_id=sender)
        pass