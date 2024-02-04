from enum import Enum
import json

class MessageType(Enum):
    RUST_IN_GAME_MSG = "rust_chat_msg",
    RUST_TEAM_CHANGE = "rust_team_change"
    
class Message:
    def __init__(self, message_type: MessageType, data: dict):
        self.type = message_type
        self.data = data
        
    def to_json(self):
        return json.dumps({"type": self.type.value, "data": self.data})

    @staticmethod
    def from_json(json_str):
        msg_dict = json.loads(json_str)
        return Message(MessageType(msg_dict["type"]), msg_dict["data"])
    
    def __str__(self):
        return self.to_json()