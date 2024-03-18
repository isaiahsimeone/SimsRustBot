from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from web.web_server_service import WebServerService
import os
import re
from urllib.parse import urlencode
from flask import Flask, redirect, render_template, request, session, make_response, jsonify, url_for

import time

import requests

from log.loggable import Loggable
from util.tools import Tools

import urllib.request

class WebRoutes(Loggable):
    
    STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'
    
    def __init__(self, app: Flask, web_server: WebServerService) -> None:
        self.app = app
        self.web_server = web_server
        self.register_routes()
        
    def register_routes(self):
        self.app.add_url_rule("/", "index", self.index, methods=["GET"])
        self.app.add_url_rule("/auth", "steam_auth", self.steam_auth, methods=["GET"])
        self.app.add_url_rule("/auth/response", "steam_auth_response", self.steam_auth_response, methods=["GET"])
        self.app.add_url_rule("/downloadsteamimage/<steam_id>", "download_steam_image", methods=["POST"])

    def index(self):
        steam_id = session.get("steam_id", None)
        # User must authenticate with steam
        if not steam_id:
            return render_template("steam_login.html")
        
        self.debug("Got steamId:", steam_id)
        
        self.debug("Waiting for page to be ready...")
        # wait
        self.debug("Page is ready")
        
        response = make_response(render_template("index.html"))
        response.set_cookie("steam_id", steam_id)
        return response
        
    def steam_auth(self):
        realm = f"http://{self.web_server.host}:{self.web_server.port}"
        params = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.mode": "checkid_setup",
            "openid.return_to": f"{realm}/auth/response",
            "openid.realm": f"{realm}/",
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        }
        return redirect(WebRoutes.STEAM_OPENID_URL + '?' + urlencode(params))

    def steam_auth_response(self):
        args = {key: val for key, val in request.args.items()}
        args["openid.mode"] = "check_authentication"
        response = requests.post(WebRoutes.STEAM_OPENID_URL, args)
        
        if "is_valid:true" in response.text:
            # Extract Steam ID from the `openid.claimed_id` returned by Steam
            match = re.search(r'https://steamcommunity.com/openid/id/(.*?)$', args["openid.claimed_id"])
            if match:
                steam_id = match.group(1)
                
                #If this user is not in the rust team, they may not access the page
                if int(steam_id) not in self.web_server.permissions:
                    print("PERMS:",self.web_server.permissions)
                    self.warning(f"Someone (steamId: {steam_id}) outside of the team attempted to access the web service")
                    return "You are not part of the team. You may not access this", 403
                
                session["steam_id"] = steam_id
                
                return redirect(url_for("index"))
                
        return "Failed to log in with Steam", 400
        
    def download_steam_image(self, steam_id):
        # Define the path where the image will be saved
        save_path = "web/static/images/steam_pics/" + steam_id + ".png"
        api_key = self.web_server.steam_api_key
        
        # Check if the file already exists
        if os.path.exists(save_path):
            self.debug(f"Steam image for {steam_id} is already downloaded")
            return jsonify({"success": True, "message": "Image already downloaded."})

        if not api_key:
            self.error(f"No steam API key is available")
            return jsonify({"success": False, "message": "No Steam API key available."}), 400

        self.debug("Requesting download of steam picture for ID:", steam_id)
        steam_info_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            'key': api_key,
            'steamids': steam_id
        }

        try:
            steam_info_response = requests.get(steam_info_url, params=params)
            steam_info_response.raise_for_status()  # Raises HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            self.error(f"Received a request error when downloading steam image: {str(e)}")
            return jsonify({"success": False, "message": str(e)}), 500

        steam_data = steam_info_response.json()
        players = steam_data.get('response', {}).get('players', [])
        
        if not players:
            return jsonify({"success": False, "message": "Player data not found."}), 404

        # Get the users avatar image
        profile_url = players[0].get('avatarfull')
        if not profile_url:
            self.error(f"Profile picture URL not found for {steam_id}")
            return jsonify({"success": False, "message": "Profile picture URL not found."}), 404

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            # Download the user's steam pic
            urllib.request.urlretrieve(profile_url, save_path)
        except Exception as e:
            self.error(f"Failed to download the users steam id ({steam_id})")
            return jsonify({"success": False, "message": "Failed to download or save image: " + str(e)}), 500

        self.debug(f"Downloaded steam image for {steam_id}")
        return jsonify({"success": True, "message": "Image downloaded successfully"})
