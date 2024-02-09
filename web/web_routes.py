from flask import render_template, request, Response, stream_with_context
from ipc.messenger import Service
import json
import time
import asyncio
from ipc.message import Message, MessageType
def setup_routes(app, web_server):
    @app.route('/')
    def index():
        
        asyncio.run(web_server.send_message(Message(MessageType.REQUEST_RUST_MAP_MONUMENTS, {}), target_service_id=Service.RUSTAPI))
        return render_template("index.html")

    @app.route('/submit_command')
    def submit_command():
        command = request.args.get('command')
        web_server.log(f"Got cmd '{command}'")
        web_server.send_message(command)
        return f"Command '{command}' received"

    @app.route('/monuments')
    def get_monuments():
        while not web_server.map_monuments:
            pass
        return web_server.map_monuments
    
    @app.route('/mapinfo')
    def get_map_info():
        while not web_server.map_info:
            pass
        return web_server.map_info