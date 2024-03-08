from enum import Enum
import json
from .serialiser import serialise_API_object
from pydantic import ValidationError

from .message_type import MessageType

class Message:
    def __init__(self, message_type: MessageType, data: dict):
        self.type = message_type
        
        # Access the Pydantic model directly from the MessageType enum
        model = self.type.model
        if model:
            try:
                # Validate data against the Pydantic model
                self.data = model(**data).dict()
            except ValidationError as e:
                raise ValueError(f"Invalid data for message type {self.type.name}: {e}")
        else:
            self.data = data

    def to_json(self):
        return json.dumps({"type": self.type.value, "data": self.data})

    @staticmethod
    def from_json(json_str: str):
        msg_dict = json.loads(json_str)
        message_type = MessageType(msg_dict["type"])
        data = msg_dict["data"]
        return Message(message_type, data)

    def __str__(self):
        return self.to_json()