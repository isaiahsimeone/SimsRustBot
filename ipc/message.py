from enum import Enum
import json
from .serialiser import serialise_API_object

class MessageType(Enum):
    RUST_IN_GAME_MSG = "rust_chat_msg",
    RUST_TEAM_CHANGE = "rust_team_change",
    
    RUST_MAP_MARKERS = "rust_map_markers",
    RUST_MAP_EVENTS = "rust_map_events"

"""
    PlayerMarker = 1
    ExplosionMarker = 2
    VendingMachineMarker = 3
    ChinookMarker = 4
    CargoShipMarker = 5
    CrateMarker = 6
    RadiusMarker = 7
    PatrolHelicopterMarker = 8

"""    

class Message:
    def __init__(self, message_type: MessageType, data: dict):
        self.type = message_type
        self.data = data
        
    def to_json(self):
        # Serialize each item in the data dictionary
        serialized_data = {k: serialise_API_object(v) for k, v in self.data.items()}
        return json.dumps({"type": self.type.value, "data": serialized_data})


    @staticmethod
    def from_json(json_str):
        msg_dict = json.loads(json_str)
        return Message(MessageType(msg_dict["type"]), msg_dict["data"])
    
    def __str__(self):
        return self.to_json()