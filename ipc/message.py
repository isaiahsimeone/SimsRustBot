from __future__ import annotations

import json
import uuid
from typing import TYPE_CHECKING, Any

from log.log_config import get_colourised_name

from .serialiser import serialise_API_object

if TYPE_CHECKING:
    from ipc.data_models import BaseModel


class Message:
    def __init__(self: Message, data: BaseModel, publisher: str | None = None, reply_to: str | None = None) -> None:
        self.id = str(uuid.uuid4())
        self.publisher = publisher
        self.raw_data = data
        self.model_data: dict[str, Any] = data.model_dump()
        self.model_type = data.__class__.__name__

    def to_json(self: Message) -> str:
        """Convert the provided :class:`Message <ipc.message.Message> to
        JSON formatted string.

        :param self: This instance
        :type self: :class:`Message <ipc.message.Message>
        :return: A JSON string
        :rtype: str
        """
        serialised_data = {k: serialise_API_object(v) for k, v in self.data.items()}
        return json.dumps({"id": self.id, "type": self.type, "data": serialised_data})

    def __str__(self: Message) -> str:
        """Return the :class:`Message <ipc.message.Message> in
        a string format.

        :return: The provided message as a string
        :rtype: str
        """
        return f"Message[Id={self.id}, type={self.type}, publisher={get_colourised_name(self.publisher)}, {self.raw_data}]"

    @property
    def data(self: Message) -> dict[str, Any]:
        return self.model_data
    
    @property
    def type(self: Message) -> str:
        return self.model_type