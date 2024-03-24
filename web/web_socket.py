from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from web.web_server_service import WebServerService
    from flask import Flask

from flask_socketio import SocketIO, emit
from log.loggable import Loggable

import json
class WebSocket(Loggable):
    def __init__(self, app: Flask, web_server: WebServerService) -> None:
        self.web_server = web_server
        self.socketio = SocketIO(app, async_mode="threading")
        
        self.socketio_init()
        
    def socketio_init(self) -> None:
        self.socketio.on_event("connect", self.socketio_connect)
        self.socketio.on_event("disconnect", self.socketio_disconnect)
        self.socketio.on_event("request_topic", self.socketio_request_topic)

    def socketio_connect(self, _ = None) -> None:
        self.debug("Client connected")
    
    def socketio_disconnect(self, _ = None) -> None:
        self.debug("Client disconnected")
        
    def broadcast_socketio(self, topic: str, data: str | None) -> None:
        if not data:
            return None
        self.socketio.emit("broadcast", {"type": topic, "data": data})
        
    def socketio_request_topic(self, sent_data: dict[str, str]) -> None:
        print("Client requested:", str(sent_data))
        topic = sent_data.get("topic", None)
        last_message = None
        if topic:
            last_message = self.web_server.last_topic_message(topic)
        
        if last_message:
            data = last_message.to_json()
        else:
            data = ""
            self.error("Unable to fulfill socketio request for topic", topic)

        emit("topic_response", {"type": topic, "data": data})