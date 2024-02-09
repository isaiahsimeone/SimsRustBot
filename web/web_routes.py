import re
from flask import render_template, request, session, redirect, url_for
import requests
from ipc.messenger import Service
import json
import time
import asyncio
from ipc.message import Message, MessageType

STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'


def setup_routes(app, web_server):
    
    @app.route('/')
    def index():
        steam_id = session.get('steam_id')
        if steam_id:
            # User is logged in fetch more details if needed        
            return render_template("index.html", steam_id=steam_id)
        return render_template("steam_login.html")
    
    @app.route('/auth')
    def auth():
        host_port = web_server.get_host() + ":" + web_server.get_port()
        params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': f'http://{host_port}/auth/response',
            'openid.realm': f'http://{host_port}/',
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        }
        return redirect(STEAM_OPENID_URL + '?' + requests.compat.urlencode(params))

    @app.route('/auth/response')
    def auth_response():
        # Validate response
        args = {key: val for key, val in request.args.items()}
        args['openid.mode'] = 'check_authentication'
        response = requests.post(STEAM_OPENID_URL, args)
        if 'is_valid:true' in response.text:
            # Extract Steam ID from the `openid.claimed_id` returned by Steam
            match = re.search(r'https://steamcommunity.com/openid/id/(.*?)$', args['openid.claimed_id'])
            if match:
                steam_id = match.group(1)
                session['steam_id'] = steam_id
                return redirect(url_for('index'))
        return 'Failed to log in with Steam', 400

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