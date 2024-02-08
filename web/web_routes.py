from flask import render_template, request, Response, stream_with_context
from ipc.messenger import Service
import json
import time

def setup_routes(app, web_server):
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/submit_command')
    def submit_command():
        command = request.args.get('command')
        web_server.log(f"Got cmd '{command}'")
        web_server.send_message(command)
        return f"Command '{command}' received"

    