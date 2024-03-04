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
    RUST_SERVER_INFO = "rust_server_info"
    RUST_TEAM_INFO = "rust_team_info"
    RUST_TEAM_CHAT_INIT = "rust_team_chat_init"
    
    # Heli
    RUST_HELI_SPAWNED = "rust_heli_spawned"
    RUST_HELI_DOWNED = "rust_heli_downed"
    RUST_HELI_DESPAWNED = "rust_heli_despawned"
    
    # Cargo
    RUST_CARGO_SPAWNED = "rust_cargo_spawned"
    RUST_CARGO_DESPAWNED = "rust_cargo_despawned"
    
    RUST_PLAYER_STATE_CHANGE = "rust_player_state_change"
    
    # Request
    REQUEST_RUST_SERVER_MAP = "request_rust_server_map"
    REQUEST_RUST_MAP_MARKERS = "request_rust_map_markers"
    REQUEST_RUST_MAP_EVENTS = "request_rust_map_events"
    REQUEST_RUST_MAP_MONUMENTS = "request_rust_map_monuments"
    REQUEST_RUST_SERVER_INFO = "request_rust_server_info"
    REQUEST_RUST_TEAM_INFO = "request_rust_team_info"
    REQUEST_RUST_TEAM_CHAT_INIT = "request_team_chat_init"
    

    # For the API to do
    SEND_TEAM_MESSAGE = "send_team_message"


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