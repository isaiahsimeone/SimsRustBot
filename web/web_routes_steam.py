import re
from flask import request, session, redirect, url_for, jsonify
import requests
import os
import urllib.request

STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'

def setup_steam_routes(app, web_server):
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
                        
                return redirect(url_for('index'))
                
        return 'Failed to log in with Steam', 400
    
    @app.route('/downloadsteamimage/<steam_id>', methods=['POST'])
    def download_steam_pic(steam_id):
        # Define the path where the image will be saved
        save_path = "web/static/images/steam_pics/" + steam_id + ".png"

        # Check if the file already exists
        if os.path.exists(save_path):
            return jsonify({"success": True, "message": "Image already downloaded."})

        if not web_server.get_steam_api_key():
            return jsonify({"success": False, "message": "No Steam API key available."}), 400

        print("REQUESTING DOWNLOAD OF STEAM PIC FOR STEAMID:", steam_id)
        steam_info_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            'key': web_server.get_steam_api_key(),
            'steamids': steam_id
        }

        try:
            steam_info_response = requests.get(steam_info_url, params=params)
            steam_info_response.raise_for_status()  # Raises a HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            return jsonify({"success": False, "message": str(e)}), 500

        steam_data = steam_info_response.json()
        players = steam_data.get('response', {}).get('players', [])
        
        if not players:
            return jsonify({"success": False, "message": "Player data not found."}), 404

        profile_url = players[0].get('avatarfull')  # Get the full-sized avatar
        if not profile_url:
            return jsonify({"success": False, "message": "Profile picture URL not found."}), 404

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            # Download the user's Steam pic
            urllib.request.urlretrieve(profile_url, save_path)
        except Exception as e:
            return jsonify({"success": False, "message": "Failed to download or save image: " + str(e)}), 500

        return jsonify({"success": True, "message": "Image downloaded successfully"})