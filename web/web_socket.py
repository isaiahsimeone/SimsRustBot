from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from web.web_server_service import WebServerService
    from flask import Flask

from flask_socketio import SocketIO, emit
from log.loggable import Loggable


class WebSocket(Loggable):
    def __init__(self, app: Flask, web_server: WebServerService) -> None:
        self.web_server = web_server
        self.socketio = SocketIO(app, async_mode="asyncio")
        
        self.socketio_init()
        
    def socketio_init(self) -> None:
        self.socketio.on_event("connect", self.socketio_connect)
        self.socketio.on_event("disconnect", self.socketio_disconnect)
        self.socketio.on_event("request_topic", self.socketio_request_topic)

    async def socketio_connect(self, _ = None) -> None:
        self.debug("Client connected")
    
    async def socketio_disconnect(self, _ = None) -> None:
        self.debug("Client disconnected")
        
    def broadcast_socketio(self, data: str) -> None:
        pass
        
    async def socketio_request_topic(self, json: dict[str, str]) -> None:
        print("Request:", str(json))
        topic = json.get("topic", None)
        if not topic:
            return None
        #data = await self.web_server.last_topic_message_or_wait("topic")
        
        last_message = await self.web_server.last_topic_message_or_wait(topic)
        data = last_message.to_json()
        emit("topic_response", {"type": topic, "data": data})