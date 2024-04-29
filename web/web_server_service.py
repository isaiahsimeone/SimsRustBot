
from __future__ import annotations
import asyncio
from io import BytesIO
import threading
from typing import TYPE_CHECKING, List

from flask import app
import loguru

from ipc.data_models import RustBackground, RustMonuments
from rust_socket.rust_socket_manager import RustSocketManager
from web.web_routes import WebRoutes
from web.web_socket import WebSocket
if TYPE_CHECKING:
    pass
from flask import Flask
from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable
from PIL import Image

from rustplus import RustSocket

from rustplus.api.structures.rust_team_info import RustTeamInfo, RustTeamMember, RustTeamNote
from rustplus.api.structures.rust_map import RustMap, RustMonument

app = Flask(__name__)
app.secret_key = 'secret'

class WebServerService(BusSubscriber, Loggable):
    def __init__(self: WebServerService, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocketManager
        
        self.team_info: RustTeamInfo
        
        self.map: RustMap 
        self.monuments: List[RustMonument]
        
        """Maps a steam ID to permissions"""
        self._permissions: dict[int, int] = {}
        """Steam API key"""
        self._steam_api_key: str = ""
        """Host that the server runs on"""
        self._host: str = "localhost"
        """Port that the server runs on"""
        self._port: int = 5000
        
        self.routes: WebRoutes
        self.sockio: WebSocket
    
    @loguru.logger.catch
    async def execute(self: WebServerService) -> None:
        await self.subscribe("server_reload")
        await self.subscribe("team_joined")
        await self.subscribe("team_left")
        await self.subscribe("team_member_join")
        await self.subscribe("team_member_left")
        await self.subscribe("team_member_vital")
        await self.subscribe("team_member_connectivity")
        await self.subscribe("team_leader_changed")
        await self.subscribe("cargo_spawned")
        await self.subscribe("cargo_despawned")
        await self.subscribe("heli_spawned")
        await self.subscribe("heli_despawned")
        await self.subscribe("heli_downed")
        await self.subscribe("chinook_spawned")
        await self.subscribe("chinook_despawned")
        await self.subscribe("chinook_downed")
        await self.subscribe("explosion")
        await self.subscribe("crate_dropped")
        await self.subscribe("marker_expired")
        await self.subscribe("map_markers")
        await self.subscribe("team_map_notes")
        await self.subscribe("team_message")
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        # Check if the service is enabled in the config
        enabled = self.config["WebServerService"]["enabled"]
        if enabled == "false":
            self.info("Service disabled in config")
            return None
        
        self._steam_api_key = self.config["WebServerService"]["steam_api_key"]
        if self._steam_api_key == "":
            self.error("No steam API key is set. No web server will be started")
            return None
        
        # Get relevant config
        self._port = int(self.config["WebServerService"].get("port", 5000))
        self._host = self.config["WebServerService"].get("host", "localhost")
        
        self.sockio = WebSocket(app, web_server=self)
        
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = await RustSocketManager.get_instance()
         # Get server info - RustPlusAPIService publishes this on startup to save tokens
        self.server_info = (await self.last_topic_message_or_wait("server_info")).data["server_info"]
        # Get team info
        self.team_info = (await self.last_topic_message_or_wait("team_info")).data["team_info"]
        
        # Set initial permissions for those in team
        for member in self.team_info.members:
            self._permissions[member.steam_id] = 1
            
        # Download the server map and monuments
        rust_map: RustMap = await self.socket.get_raw_map_data()
        
        # Monuments
        await self.publish("monuments", RustMonuments(monuments=rust_map.monuments))
        
        # Background colour of map
        await self.publish("background", RustBackground(background=rust_map.background))
        
        # Save the map image
        map_image = Image.open(BytesIO(rust_map.jpg_image))
        cropped = map_image.crop((500, 500, rust_map.width - 500, rust_map.height - 500))
        resized = cropped.resize((2000, 2000), Image.LANCZOS).convert("RGB")
        
        resized.save("web/static/images/map.jpg")
        
        self.routes = WebRoutes(app, web_server=self)
        
        await self.webserver_main()
        
    async def webserver_main(self: WebServerService):
        threading.Thread(target=lambda: app.run(host=self._host, port=self._port, debug=True, use_reloader=False, threaded=True)).start()
        self.info(f"Server started http://{self._host}:{self._port}")
        
        await asyncio.Future()
    
    @property
    def port(self: WebServerService) -> int:
        return self._port
    
    @property
    def host(self: WebServerService) -> str:
        return self._host
    
    @property
    def permissions(self: WebServerService) -> dict[int, int]:
        return self._permissions
    
    @property
    def steam_api_key(self: WebServerService) -> str:
        return self._steam_api_key
    
    @loguru.logger.catch
    async def on_message(self: WebServerService, topic: str, message: Message):
        match topic:
            case "team_joined":
                self.debug("joined a team")
                self.team_info: RustTeamInfo = (await self.last_topic_message_or_wait("team_info")).data["team_info"]
                for member in self.team_info.members:
                    self._permissions[member.steam_id] = 1
            case "team_left":
                self.debug("left a team")
                self._permissions = {}
                self.team_info: RustTeamInfo = (await self.last_topic_message_or_wait("team_info")).data["team_info"]
                for member in self.team_info.members:
                    self._permissions[member.steam_id] = 1
            case "team_member_join":
                self.debug("Team member joined")
                member: RustTeamMember = message.data["member"]
                self._permissions[member.steam_id] = 1
            case "team_member_left":
                self.debug("team member left")
                member: RustTeamMember = message.data["member"]
                del self._permissions[member.steam_id]
            case "server_reload":
                self.info("Web server should reload")
            case "team_map_notes":
                pass
            case "team_member_vital":
                pass
            case "team_member_connectivity":
                pass
            case "team_leader_changed":
                pass
            case "map_markers":
                pass
            case "heli_spawned" | "heli_despawned" | "heli_downed":
                pass
            case "cargo_spawned" | "cargo_despawned":
                pass
            case "explosion" | "marker_expired":
                pass
            case "chinook_spawned" | "chinook_downed" | "chinook_despawned" | "crate_dropped":
                pass
            case "team_message":
                pass
            case _:
                self.error(f"Got a message (topic {topic}) from bus that doesn't have an implementation")
            
        self.sockio.broadcast_socketio(topic, message.to_json())