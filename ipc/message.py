import json
import uuid
from ipc.data_models import BaseModel
from log.log_config import get_colourised_name
from .serialiser import serialise_API_object

from .message_type import MessageType

class Message:
    def __init__(self, data: BaseModel, publisher: str = None, reply_to: str = None): # type: ignore
        self.id = str(uuid.uuid4())
        self.publisher = publisher
        self.reply_to = reply_to # Identifier correlating rteplies with this message
        self.raw_data = data
        self.data = data.model_dump()  # If you need the data as a dictionary
        self.type = data.__class__.__name__
        
    def to_json(self):
        serialised_data = {k: serialise_API_object(v) for k, v in self.data.items()}
        return json.dumps({"id": self.id, "type": self.type, "data": serialised_data})

    @staticmethod
    def from_json(json_str: str):
        msg_dict = json.loads(json_str)
        message_type = MessageType(msg_dict["type"])
        # You'll need to adapt this part to properly reconstruct the BaseModel from `data`
        data_model = message_type.model.from_dict(msg_dict["data"])  # This is a placeholder
        message = Message(data_model)
        message.id = msg_dict.get('id', '')
        return message

    def __str__(self): 
        return f"Message[Id={self.id}, type={self.type}, publisher={get_colourised_name(self.publisher)}, {self.raw_data}]"