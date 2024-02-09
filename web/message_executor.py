from ipc.message import MessageType as MT
from ipc.message import Message
from ipc.messenger import Service
from PIL import Image 

class MessageExecutor():
    def __init__(self, web_server):
        self.web_server = web_server
                    
    def get_message_type(self, value):
        for member in MT:
            if member.value == value:
                return member
        return None
    
    async def execute_message(self, msg, sender):
        data = msg.get("data")
        msg_type = self.get_message_type(msg.get("type"))
        
        match msg_type:
            case MT.RUST_IN_GAME_MSG:
                print("In game message handler")
            case MT.RUST_SERVER_MAP:
                self.web_server.log("Got server map. Moving to images root")
                self.receive_map_image(data)
            case MT.RUST_MAP_MARKERS:
                self.web_server.log("Updating map markers")
                self.receive_map_markers(data)
            case MT.RUST_MAP_MONUMENTS:
                self.web_server.log("Received map monuments")
                self.receive_map_monuments(data)
            case MT.RUST_PLAYER_STATE_CHANGE:
                self.web_server.log("Got a player state change")
                self.receive_player_state_change(data)
            case _:
                self.web_server.log("ERROR: Unknown message type")

    def receive_map_image(self, data):
        image_data = data.get("data")
        
        img_width = image_data.get("width")
        img_height = image_data.get("height")
        img_pixels = [tuple(pixel) for pixel in image_data.get("pixels")]
        
        img = Image.new(mode="RGB", size=(img_width, img_height))
        img.putdata(img_pixels)
        
        img.save("web/static/images/map.jpg")
        
    def receive_map_markers(self, data):
        self.web_server.map_markers_queue.append(data.get("markers"))
        
    def receive_map_monuments(self, data):
        self.web_server.map_monuments = data
    
    def receive_player_state_change(self, data):
        self.web_server.team_update_queue.append(data)