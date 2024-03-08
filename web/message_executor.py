from __future__ import annotations
from base64 import b64decode
from io import BytesIO
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ipc.bus import BUS
    from web_server import WebServer

from ipc.message import MessageType as MT
from ipc.message import Message
from ipc.bus import Service
from PIL import Image

from util.loggable import Loggable 

class MessageExecutor(Loggable):
    def __init__(self, web_server: WebServer):
        self.web_server = web_server
        super().__init__(web_server.log)

    def get_message_type(self, value):
        for member in MT:
            if member.value == value:
                return member
        return None
    
    async def execute_message(self, msg, sender):
        data = msg.get("data")
        msg_type = self.get_message_type(msg.get("type"))
        
        match msg_type:
            case MT.RUST_TEAM_CHAT_INIT:
                self.log("Got initial team chat")
                self.receive_team_chat_init(data)
            case MT.RUST_CHAT_MESSAGE:
                self.log("Got a team chat")
                self.receive_team_chat(data)
            case MT.RUST_SERVER_MAP:
                self.log("Got server map. Moving to images root")
                self.receive_map_image(data)
            case MT.RUST_MAP_MARKERS:
                self.log("Updating map markers")
                self.receive_map_markers(data)
            case MT.RUST_MAP_MONUMENTS:
                self.log("Received map monuments")
                self.receive_map_monuments(data)
            case MT.RUST_PLAYER_STATE_CHANGE:
                self.log("Got a player state change")
                self.receive_player_state_change(data)
            case MT.RUST_SERVER_INFO:
                self.log("Got Server Info")
                self.receive_server_info(data)
            case MT.RUST_TEAM_INFO:
                self.log("Got team info")
                self.receive_team_info(data)
            #case MT.RUST_HELI_DOWNED:
            #    self.web_server.log("Heli went down")
            #case MT.RUST_CARGO_SPAWNED:
            #    self.web_server.log("Cargo spawned")
            case _:
                self.log(f"Unknown message type: {msg_type}", type="error")

    def receive_map_image(self, data):
        encoded_pixels = data.get("pixels")
 
        # Decode the base64-encoded pixel data to get the raw image bytes
        pixels = b64decode(encoded_pixels)
        width = data.get("width")
        height = data.get("height")
        
        image = Image.open(BytesIO(pixels))
        
        cropped = image.crop((500, 500, width - 500, height - 500))
        resized = cropped.resize((2000, 2000), Image.LANCZOS).convert("RGB")
        
        # Optionally, if you want to ensure the image is in a specific mode, you can convert it
        # However, this step may not be necessary if the image is already in the desired format
        #img = img.convert('RGB')
        
        # Save the image to your desired path
        resized.save("web/static/images/map.jpg")
        
        # Set the flag indicating the map image is available
        self.web_server.map_image_available = True
        
    def receive_map_markers(self, data):
        self.web_server.map_marker_data = data.get("markers")
        self.web_server.broadcast_to_web("markers", data.get("markers"))
        
    def receive_map_monuments(self, data):
        self.web_server.map_monuments = data
        self.web_server.broadcast_to_web("monuments", data)
    
    def receive_player_state_change(self, data):
        self.web_server.team_update_queue.append(data)
        #TODO: ??????
        
    def receive_server_info(self, data):
        self.web_server.server_info = data
        self.web_server.broadcast_to_web("serverinfo", data)
        
    def receive_team_info(self, data):
        self.web_server.team_info = data
        self.web_server.broadcast_to_web("teaminfo", data)
        
    def receive_team_chat_init(self, data):
        if not data:
            return  # Probably isn't in a team
        self.log("GOT: " + str(data))
        for message in data:
            self.log("-", str(message))
            self.web_server.team_chat_log.append(message)
    
    def receive_team_chat(self, data):
        self.log("GOTTC: " + str(data))
        self.web_server.team_chat_log.append(data)
        self.web_server.broadcast_to_web("teamchat", data)