from __future__ import annotations
import asyncio
import json
import time
from typing import TYPE_CHECKING

from flask import request, session

from ipc.data_models import BaseModel, Empty, PlayerFcmToken, PlayerServerToken, RustTeamChatMessage
from ipc.message import Message
if TYPE_CHECKING:
    from web.web_server_service import WebServerService
    from flask import Flask

from flask_socketio import SocketIO, emit
from log.loggable import Loggable

# Rate limiting parameters - MESSAGE_LIMIT messages in TIME_PERIOD seconds, or blocked for BLOCK_TIME
MESSAGE_LIMIT = 10
TIME_PERIOD = 5
BLOCK_TIME = 40  # seconds

class WebSocket(Loggable):
    def __init__(self, app: Flask, web_server: WebServerService) -> None:
        self.web_server = web_server
        self.socketio = SocketIO(app, async_mode="threading")
        
        self.client_messages = {}
            
        self.socketio_init()
        
    def socketio_init(self) -> None:
        self.socketio.on_event("connect", self.socketio_connect)
        self.socketio.on_event("disconnect", self.socketio_disconnect)
        self.socketio.on_event("request_topic", self.socketio_request_topic)
        self.socketio.on_event("client_send", self.socketio_from_client)

    def socketio_connect(self, _ = None) -> None:
        self.debug("Client connected")
    
    def socketio_disconnect(self, _ = None) -> None:
        self.debug("Client disconnected")
        
    def broadcast_socketio(self, topic: str, data: str | None) -> None:
        if not data:
            return None
        self.socketio.emit("broadcast", {"type": topic, "data": data})
    
    
    def socketio_from_client(self, data: dict) -> None:
        def is_rate_limited(sid) -> bool:
            current_time = time.time()
            timestamps = self.client_messages.get(sid, [])

            # Remove timestamps older than the time period
            timestamps = [t for t in timestamps if current_time - t < TIME_PERIOD]
            self.client_messages[sid] = timestamps

            # Check if client is currently blocked
            if 'block_until' in session and session['block_until'] > current_time:
                return True

            # Check if message limit is exceeded
            if len(timestamps) >= MESSAGE_LIMIT:
                session['block_until'] = current_time + BLOCK_TIME
                return True

            # Add the current timestamp and allow the message
            timestamps.append(current_time)
            return False
                
        sid = request.sid # type: ignore
        
        if is_rate_limited(sid):
            self.warning(f"Rate limited sid={sid}, ipv4={request.remote_addr}")
            return None
            
        if not data:
            return None
        
        try:
            topic = data.get("topic")
            msg = data.get("data")

            if not msg:
                self.debug("Error: Submitted data contains no key 'data'")
                return None
            
            if not isinstance(msg, dict):
                self.debug("Error: 'data' is expected to be a dictionary.")
                return None
            
            model: BaseModel = Empty()
            # Publish to the bus
            match topic:
                case "player_server_token":
                    raw_token = json.loads(msg["token"])
                    sender_steam_id = msg["steam_id"]
                    
                    desc, id, img, ip, logo, name, steam_id, playerToken, port, type_, url = (
                        raw_token[k] for k in ["desc", "id", "img", "ip", "logo", "name", "playerId", "playerToken", "port", "type", "url"]
                    )
                    
                    if sender_steam_id != steam_id:
                        self.warning("Someone tried to submit a server token for a steam ID that isn't their own")
                        return None
                    
                    model = PlayerServerToken(desc=desc, id=id, img=img, ip=ip, logo=logo, name=name, 
                                              steam_id=steam_id, playerToken=playerToken, port=port, type_=type_, url=url)
                    
                case "player_fcm_token":
                    model = PlayerFcmToken(steam_id=msg["steam_id"], token=msg["token"].strip().replace("\n", ""))
                case "send_player_message":
                    model = RustTeamChatMessage(steam_id=msg["steam_id"], name=msg["name"], message=msg["message"],
                                                colour=msg["colour"], time=int(msg["time"]))
                case _:
                    self.error(f"Got client topic/data that can't be handled in match - Can't handle topic '{topic}'")
                    return None

            asyncio.run(self.web_server.publish(topic, model))

        except Exception as e:
            self.error(e)
            self.debug(f"DBGERROR: Unable to handle client socketio submission")
            return None
        
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