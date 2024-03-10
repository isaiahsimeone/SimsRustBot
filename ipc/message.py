from enum import Enum
import json

from ipc.data_models import BaseModel
from .serialiser import serialise_API_object
from pydantic import ValidationError

from .message_type import MessageType

class Message:
    def __init__(self, message_type: MessageType, data: BaseModel):
        self.type = message_type

        # Ensure the data is an instance of the expected model
        expected_model = self.type.model
        if not isinstance(data, expected_model):
            raise ValueError(f"Data must be an instance of {expected_model.__name__}")

        self.data = data.model_dump()  # If you need the data as a dictionary

    def to_json(self):
        # Serialize each item in the data dictionary
        serialised_data = {k: serialise_API_object(v) for k, v in self.data.items()}
        return json.dumps({"type": self.type.value, "data": serialised_data})

    @staticmethod
    def from_json(json_str: str):
        msg_dict = json.loads(json_str)
        message_type = MessageType(msg_dict["type"])
        data = msg_dict["data"]
        return Message(message_type, data)

    def __str__(self):
        return self.to_json()