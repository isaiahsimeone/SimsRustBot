from enum import Enum
import json
from .serialiser import serialise_API_object

class MessageType(Enum):
    RUST_IN_GAME_MSG = "rust_chat_msg"
    RUST_TEAM_CHANGE = "rust_team_change"
    
    RUST_SERVER_MAP = "rust_server_map"
    RUST_MAP_MARKERS = "rust_map_markers"
    RUST_MAP_EVENTS = "rust_map_events"
    RUST_MAP_MONUMENTS = "rust_map_monuments"
    
    # Request
    REQUEST_RUST_SERVER_MAP = "request_rust_server_map"
    REQUEST_RUST_MAP_MARKERS = "request_rust_map_markers"
    REQUEST_RUST_MAP_EVENTS = "request_rust_map_events"
    REQUEST_RUST_MAP_MONUMENTS = "request_rust_map_monuments"

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
        self.data = dict() if data is None else data
    
    def set_type(self, t):
        self.type = t
        
    def set_data(self, d):
        self.data = dict() if d is None else d
    
    def to_json(self):
        # Serialize each item in the data dictionary
        serialised_data = {k: serialise_API_object(v) for k, v in self.data.items()}
        return json.dumps({"type": self.type.value, "data": serialised_data})

    @staticmethod
    def from_json(json_str):
        msg_dict = json.loads(json_str)
        return Message(MessageType(msg_dict["type"]), msg_dict["data"])
    
    def __str__(self):
        return self.to_json()