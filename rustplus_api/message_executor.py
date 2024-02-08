from ipc.message import MessageType as MT
from PIL import Image 

from ipc.message import Message, MessageType

from .commands import get_server_map

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
        print("GOT MSG: " + msg.from_json())
        msg_type = self.get_message_type(msg.get("type"))
        
        match msg_type:
            case MT.REQUEST_RUST_SERVER_MAP:
                self.send_server_map_image(sender)

            case None:
                self.api.messenger.print("ERROR: Unknown message type")

    async def get_server_map_image(self, sender):
        print("SENDING MAP")
        server_map = await get_server_map(self.socket)
        message = Message(MessageType.RUST_SERVER_MAP, {"data": server_map})
        await self.api.send_message(message, sender=sender)
        
        
    