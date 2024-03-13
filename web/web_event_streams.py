from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ipc.message_bus import MessageBus
    from web_server import WebServer



from flask import render_template, Response, stream_with_context
from flask_socketio import emit
from ipc.data_models import RustChatMessage, RustRequestSendTeamMessage, RustTeamChatMessage
from ipc.message import Message, MessageType
from ipc.message_bus import Service
import json
import time
import asyncio
from ipc.serialiser import serialise_API_object
from util.tools import Tools

def setup_event_streams(socketio, web_server: WebServer):
    
    @socketio.on('connect')
    def socketio_connect():
        print("Client connected")
        
    @socketio.on('disconnect')
    def socketio_disconnect():
        print("Client disconnected")
        
    @socketio.on('request')
    def request_data(message):
        request_what = message.get("type")
        data = {}
        
        match request_what:
            case "teamchat":
                data = web_server.team_chat_log
            case "monuments":
                data = web_server.map_monuments
            case "markers":
                data = web_server.map_marker_data
            case "serverinfo":
                data = web_server.server_info
            case "teaminfo":
                data = web_server.team_info
            case "mapnotesweb":
                data = web_server.map_note_manager.get_notes()
            case _:
                web_server.log("Client requested unknown data: " + str(message), "error")
        
        emit("data_response", {"type": request_what, 
                               "data": Tools.stringify_steam_ids(data)}) # type:ignore
  
    @socketio.on('client_send')
    def client_sent_data(message):
        what = message.get("type")
        data = message.get("data")
        
        web_server.log("Client sent: " + str(what) + " " + str(data))
        
        def async_task():
            asyncio.run(process_client_transmission(what, data))
            
        socketio.start_background_task(async_task())
    
    async def process_client_transmission(what, data):
        match what:
            case "teamchat":
                message = data.get("message")
                sender = data.get("sender")
                msg = RustRequestSendTeamMessage(steam_id=0, name=sender, message=message, time=int(time.time()))
                await web_server.send_message(Message(MessageType.REQUEST_SEND_TEAM_MESSAGE, msg), Service.RUSTAPI)
            case "newmapnote":
                web_server.log("Got new map note")
                message = data.get("message")
                sender = data.get("sender")
                # No BUS message sent, this data is just for the web app currently
                web_server.map_note_manager.add_note(message, sender)
            case "removemapnote":
                web_server.log("Got request to remove map note")
                message = data.get("message")
                sender = data.get("sender")
                web_server.map_note_manager.remove_note(message, sender)
        await asyncio.sleep(1) # TODO: This is hacky. Need to wait for message to propagate to rust API listener
