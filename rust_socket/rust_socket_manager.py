
from __future__ import annotations

import asyncio


from log.loggable import Loggable
from rust_socket.client_rust_socket import ClientRustSocket


from typing import TYPE_CHECKING, List, Union
if TYPE_CHECKING:
    from rustplus.api.structures.rust_marker import RustMarker
    from rustplus.api.structures.rust_team_info import RustTeamNote
    from rustplus.api.structures.rust_team_info import RustTeamInfo

from rustplus import RustSocket
from rustplus.exceptions.exceptions import ServerNotResponsiveError

class RustSocketManager(Loggable):
    instance = None
    lock = asyncio.Lock()
    
    def __init__(self) -> None:
        self.leader_socket_initialised = False
        self.leader_socket: ClientRustSocket
        self.sockets: dict[int, ClientRustSocket] = {}
    
    async def initialise_socket_leader(self: RustSocketManager, ip: str, port: str, steam_id: int, playerToken: str) -> None:
        if self.leader_socket_initialised:
            self.warning("Leader socket already initialised")
            return None
        
        leader_socket = await self.create_and_connect_socket(ip, port, steam_id, playerToken)
        if leader_socket:
            self.leader_socket = leader_socket
        else:
            self.critical("Couldn't connect the leader socket")
        self.leader_socket_initialised = True
        
    def register_socket(self, socket: ClientRustSocket) -> None:
        pass
    
    def deregister_socket(self, socket: ClientRustSocket) -> None:
        pass
    
    @classmethod
    async def get_instance(cls: type[RustSocketManager]) -> RustSocketManager:
        async with cls.lock:
            if cls.instance is None:
                cls.instance = cls()
            return cls.instance
    
    @classmethod
    def prepare(cls: type[RustSocketManager]) -> None:
        if cls.instance is None:
            cls.instance = cls()
        else:
            cls.instance.warning("RustSocketManager is already initialised.")
    
    #### Internal methods
    
    async def create_and_connect_socket(self, ip: str, port: str, steam_id, playerToken: str):
        if self.sockets.get(steam_id):
            self.warning("This steam user already has a rust socket")
            return None
           
        rust_socket = RustSocket(ip, port, steam_id, int(playerToken))
        try:
            await rust_socket.connect(retries=20, delay=15)
        except ServerNotResponsiveError:
            self.error(f"Unable to connect to server {ip}:{port} For steam ID {steam_id}. Server is unresponsive")
        
        client_socket = ClientRustSocket(steam_id, rust_socket)
        self.sockets[steam_id] = client_socket
            
        return client_socket
    
    def client_socket_most_tokens(self) -> ClientRustSocket:
        best_candidate = self.leader_socket
        for _, value in self.sockets.items():
            if value.tokens_available() > best_candidate.tokens_available():
                best_candidate = value
        return best_candidate

     #### RustSocket methods
    
    # Any socket
    async def get_time(self):
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_time")
        return await selected_socket.socket.get_time()
    
    # Use specific socket, fallback to leader
    async def send_team_message(self, message: Union[str, object], steam_id: int | None = None):
        socket = self.sockets[steam_id] if steam_id and self.sockets[steam_id] else self.leader_socket
        self.debug("Using", socket.steam_id, "for send_team_message")
        return await socket.socket.send_team_message(message)
    
    # Use specific socket, leader is truth
    async def get_info(self, steam_id: int | None = None):
        socket = self.sockets[steam_id] if steam_id and self.sockets[steam_id] else self.leader_socket
        self.debug("Using", socket.steam_id, "for get_info")
        return await socket.socket.get_info()
    
    # Any socket
    async def get_team_chat(self):
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_team_chat")
        return await selected_socket.socket.get_team_chat()
    
    # Use specific socket, aggregate, leader is fallback
    # Todo: this might be pretty slow
    async def get_team_info(self) -> RustTeamInfo:
        team_info = await self.leader_socket.socket.get_team_info()
        team_notes: List[RustTeamNote] = []
        for _, value in self.sockets.items():
             notes = (await value.socket.get_team_info()).map_notes
             for note in notes:
                 team_notes.append(note)
        team_info._map_notes = team_notes
        return team_info
    
    # Any socket
    async def get_markers(self) -> List[RustMarker]:
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_markers")
        return await selected_socket.socket.get_markers()
    
    # Any socket
    async def get_raw_map_data(self):
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_raw_map_data")
        return await selected_socket.socket.get_raw_map_data()
    
    # Any socket
    async def get_map(self):
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_map")
        return await selected_socket.socket.get_map()
    
    # pretty sure this is socket specific
    async def get_entity_info(self):
        pass
    
    # pretty sure this is socket specific
    async def _update_smart_device(self):
        pass
    
    # pretty sure this is socket specific
    async def turn_on_smart_switch(self):
        pass
    
    # pretty sure this is socket specific
    async def turn_off_smart_switch(self):
        pass
    
    # Leader socket?
    async def promote_to_team_leader(self):
        pass
    
    # Any socket
    async def get_current_events(self):
        selected_socket = self.client_socket_most_tokens()
        self.debug("Using", selected_socket.steam_id, "for get_current_events")
        return await selected_socket.socket.get_current_events()
    
    # Specific socket, fallback to leader
    async def get_contents(self):
        pass
    
    #????????
    async def get_camera_manager(self):
        pass
    
    def __str__(self):
        s = "["
        for steam_id, rust_socket in self.sockets.items():
            s += f"SteamId: {steam_id}. RustSocket:{rust_socket.socket.server_id}\n"
        s += "]"
        return s