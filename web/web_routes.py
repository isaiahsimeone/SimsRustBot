import re
from flask import render_template, request, session, redirect, url_for, make_response, jsonify
import requests
from ipc.message_bus import Service
import json
import time
import asyncio
import os
from ipc.message import Message, MessageType
import urllib.request

from util.tools import Tools

def setup_routes(app, web_server):
    
    @app.route('/')
    def index():
        steam_id = session.get('steam_id')
        if steam_id:
            # User is logged in
            print("Got steamID: " + steam_id)
            
            # Check if the server is ready
            print("Waiting for page to be ready...")
            if not web_server.page_ready:
                return render_template("wait.html")    
            time.sleep(1)
            print("Page is ready")
            
            response = make_response(render_template("index.html"))
            response.set_cookie("steam_id", steam_id)
            return response
        return render_template("steam_login.html", steam_id=steam_id)
    
    @app.route('/check_page_ready')
    def check_page_ready():
        return jsonify({"pageReady": web_server.page_ready})
    
    @app.route('/sendteammessage', methods=['POST'])
    def send_team_message():
        
        if request.method == "POST":
            data = request.form
            
            web_server.log("Someone sent a team chat from the web server")

        return "RESPONSE"

    @app.route('/get/<what>')
    def get_data(what):
        data = None
        match what:
            case "monuments":
                data = web_server.map_monuments
            case "serverinfo":
                data = web_server.server_info
            case "teaminfo":
                data = web_server.team_info
            case "teamchat":
                data = web_server.team_chat_log
            case "markers":
                data = web_server.map_marker_data
            case _:
                return "Unknown request type: " + what, 400
        return Tools.stringify_steam_ids(data), 200

   