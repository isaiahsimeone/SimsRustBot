from ipc.message import MessageType as MT
from PIL import Image 

from ipc.message import Message, MessageType

from .commands.get_server_map import get_server_map
from .commands.get_monuments import get_monuments
from .commands.get_server_info import get_server_info
from .commands.get_team_info import get_team_info
from .commands.get_team_chat import get_team_chat

class MessageExecutor():
    def __init__(self, rust_api):
        self.api = rust_api
        self.socket = self.api.get_socket()
                    
    def get_message_type(self, value):
        for member in MT:
            if member.value == value:
                return member
        return None
    
    async def execute_message(self, msg, sender):
        msg_type = self.get_message_type(msg.get("type"))
        
        match msg_type:
            case MT.REQUEST_RUST_SERVER_MAP:
                print("I AM SENDING THE MAP")
                await self.send_server_map_image(sender)
            case MT.REQUEST_RUST_MAP_MONUMENTS:
                await self.send_server_map_monuments(sender)
            case MT.REQUEST_RUST_SERVER_INFO:
                await self.send_server_info(sender)
            case MT.REQUEST_RUST_TEAM_INFO:
                await self.send_team_info(sender)
            case MT.REQUEST_RUST_TEAM_CHAT_INIT:
                await self.send_team_chat_init(sender)
            case _:
                self.api.log("ERROR: Unknown message type")

    async def send_server_map_image(self, sender):
        server_map = await get_server_map(self.socket)
        message = Message(MessageType.RUST_SERVER_MAP, {"data": server_map})
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_server_map_monuments(self, sender):
        server_monuments = await get_monuments(self.socket)
        message = Message(MessageType.RUST_MAP_MONUMENTS, {"data": server_monuments})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_server_info(self, sender):
        server_info = await get_server_info(self.socket)
        message = Message(MessageType.RUST_SERVER_INFO, {"data": server_info})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_info(self, sender):
        team_info = await get_team_info(self.socket)
        message = Message(MessageType.RUST_TEAM_INFO, {"data": team_info})
        await self.api.send_message(message, target_service_id=sender)
        
    async def send_team_chat_init(self, sender):
        initial_team_chat = await get_team_chat(self.socket)
        message = Message(MessageType.RUST_TEAM_CHAT_INIT, {"data": initial_team_chat})
        await self.api.send_message(message, target_service_id=sender)
    