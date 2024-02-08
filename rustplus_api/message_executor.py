from ipc.message import MessageType as MT
from PIL import Image 

from ipc.message import Message, MessageType

from .commands.get_server_map import get_server_map
from .commands.get_monuments import get_monuments

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
        print("GOT MSG: " + str(msg))
        msg_type = self.get_message_type(msg.get("type"))
        
        print("is map req: " + str(msg_type == MT.REQUEST_RUST_SERVER_MAP))
        print("is mon req: " + str(msg_type == MT.REQUEST_RUST_MAP_MONUMENTS))
        
        match msg_type:
            case MT.REQUEST_RUST_SERVER_MAP:
                print("I AM SENDING THE MAP")
                await self.send_server_map_image(sender)
            case MT.REQUEST_RUST_MAP_MONUMENTS:
                await self.send_server_map_monuments(sender)
            case _:
                print("******* UNKNOWN MESSAGE : messageexecutor for api: " + str(msg_type))
                self.api.log("ERROR: Unknown message type")

    async def send_server_map_image(self, sender):
        print("SENDING MAP")
        server_map = await get_server_map(self.socket)
        message = Message(MessageType.RUST_SERVER_MAP, {"data": server_map})
        await self.api.send_message(message, target_service_id=sender)
    
    async def send_server_map_monuments(self, sender):
        server_monuments = await get_monuments(self.socket)
        message = Message(MessageType.RUST_MAP_MONUMENTS, {"data": server_monuments})
        await self.api.send_message(message, target_service_id=sender)
        
    