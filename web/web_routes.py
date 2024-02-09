import re
from flask import render_template, request, session, redirect, url_for, make_response
import requests
from ipc.messenger import Service
import json
import time
import asyncio
from ipc.message import Message, MessageType
import urllib.request
STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'


def setup_routes(app, web_server):
    
    @app.route('/')
    def index():
        steam_id = session.get('steam_id')
        if steam_id:
            print("Got steamID: " + steam_id)
            # User is logged in fetch more details if needed
            response = make_response(render_template("index.html"))
            response.set_cookie("steam_id", steam_id)
            return response
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
                
                #TODO: check if this person is in the rust UI team, if they aren't, don't forward them
                
                # Use SteamID to fetch the user's profile picture from Steam's Web API
                steam_info_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
                params = {
                    'key': web_server.get_steam_api_key(),
                    'steamids': steam_id
                }
                steam_info_response = requests.get(steam_info_url, params=params)
                if steam_info_response.status_code == 200:
                    steam_data = steam_info_response.json()
                    players = steam_data.get('response', {}).get('players', [])
                    if players:
                        profile_url = players[0].get('avatarfull')  # Get the full-sized avatar
                        
                        # Download this users steam pic
                        urllib.request.urlretrieve(profile_url, "web/static/images/steam_pics/" + steam_id + ".png")
                        
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
    
    @app.route('/serverinfo')
    def get_server_info():
        while not web_server.server_info:
            pass
        print(web_server.server_info)
        return web_server.server_info