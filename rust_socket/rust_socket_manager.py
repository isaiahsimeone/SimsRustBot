
from __future__ import annotations

import asyncio
import threading


from log.loggable import Loggable
from rust_socket.client_rust_socket import ClientRustSocket


from typing import TYPE_CHECKING, List, Union

from rust_socket.structures.extended_rust_team_note import ExtendedRustTeamNote
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
        self.loops = {}
        self.threads = {}
    
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
    
    def has_token_for_steam_id(self, steam_id) -> bool:
        self.warning("Axxx", str(steam_id) in self.sockets.keys(), " - ", self.sockets.keys())
        return str(steam_id) in self.sockets.keys()

        
    async def socket_get_with_timeout(self, client_socket, socket_method_name, timeout_seconds=2, *args, **kwargs):
        """
        Asynchronously calls a specified method on a rust socket with a timeout.

        This method dynamically retrieves and invokes a method from the client socket using the provided `socket_method_name`.
        It applies a timeout to this operation and captures any resulting errors or timeouts. The operation's results are returned 
        if successful. In case of timeouts or other exceptions, an empty list is returned.

        :param client_socket: The client socket object on which the method will be called.
        :type client_socket: ClientSocket
        :param socket_method_name: The name of the method to be called on the client socket.
        :type socket_method_name: str
        :param timeout_seconds: The maximum time in seconds to wait for the method call to complete, defaults to 2 seconds.
        :type timeout_seconds: int, optional
        :param args: Variable length argument list for the method being called.
        :param kwargs: Arbitrary keyword arguments for the method being called.
        :return: The result of the method call if successful (usually map notes), or an empty list in case of timeouts or exceptions.
        :rtype: list
        :raises asyncio.TimeoutError: If the method call exceeds the specified timeout.
        :raises Exception: For any other issues that arise during the method call.
        """
        try:
            # Get the method from the client_socket based on the method_name string
            method = getattr(client_socket.socket, socket_method_name)
            # Call the method with provided args and kwargs, with a timeout
            socket_info = await asyncio.wait_for(method(*args, **kwargs), timeout=timeout_seconds)
            self.debug("Using", client_socket.steam_id, "for", socket_method_name)
            return socket_info.map_notes
        except asyncio.TimeoutError:
            self.debug("Timeout", client_socket.steam_id)
            return []
        except Exception as e:
            self.debug("Error with", client_socket.steam_id, ":", str(e))
            return []
    
    def create_socket_thread(self, ip, port, steam_id, playerToken):
        loop = asyncio.new_event_loop()

        def thread_target():
            asyncio.set_event_loop(loop)
            self.loops[steam_id] = loop
            loop.run_until_complete(self.create_and_connect_socket(ip, port, steam_id, playerToken))
            loop.run_forever()

        thread = threading.Thread(target=thread_target)
        thread.start()
        self.threads[steam_id] = thread
    
    async def create_and_connect_socket(self, ip: str, port: str, steam_id, playerToken: str):
        self.debug("CREATING SOCKET")
        if self.sockets.get(steam_id):
            self.warning("This steam user already has a rust socket")
            return None
           
        rust_socket = RustSocket(ip, port, steam_id, int(playerToken))
        try:
            await rust_socket.connect(retries=5, delay=5)
            client_socket = ClientRustSocket(steam_id, rust_socket)
            self.sockets[steam_id] = client_socket
            
            return client_socket
        except ServerNotResponsiveError:
            self.error(f"Unable to connect to server {ip}:{port} For steam ID {steam_id}. Server is unresponsive")
        
    
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
        socket = self.leader_socket
        if steam_id and self.has_token_for_steam_id(steam_id):
            socket = self.sockets[str(steam_id)]
        elif steam_id:
            self.warning(f"Steam ID {steam_id} ({type(steam_id)}) was provided but it doesn't have an associated socket")
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
        try:
            return await selected_socket.socket.get_team_chat()
        except Exception as e:
            self.warning("Unable to get team chat. Bot operator isn't in a team. Will fetch once they're in a team")
            return []

  
    async def get_team_info(self) -> RustTeamInfo:
        # Start tasks for each socket concurrently with a timeout
        tasks = {steam_id: self.socket_get_with_timeout(socket, "get_team_info") for steam_id, socket in self.sockets.items()}
        completed_tasks = await asyncio.gather(*tasks.values(), return_exceptions=True)
        self.debug("Have sockets for:", self.sockets.keys())
        # Initialize team_info and team_notes
        team_info = await self.leader_socket.socket.get_team_info()
        team_notes = []

        # Process results, ignoring timeouts and errors, and wrap RustTeamNote with steam_id
        for steam_id, result in zip(tasks.keys(), completed_tasks):
            if isinstance(result, Exception) or isinstance(result, BaseException):
                continue  # Skip exceptions
            for note in result:  # Assuming result is a list of RustTeamNote
                enhanced_note = ExtendedRustTeamNote(note, steam_id)  # Wrap in custom class
                team_notes.append(enhanced_note)
        
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
    
    def team_event(self, callback):
        self.leader_socket.socket.team_event(callback)
        
    def chat_event(self, callback):
        self.leader_socket.socket.chat_event(callback)
        
    def protobuf_received(self, callback):
        self.leader_socket.socket.protobuf_received(callback)
    
    def register_entity_event_listener(self, callback, eid):
        self.leader_socket.socket.remote.handle_subscribing_entity(eid, callback)
    
    
    def __str__(self):
        s = "{"
        for steam_id, rust_socket in self.sockets.items():
            s += f"SteamId: {steam_id}. RustSocket:{rust_socket.socket.server_id}\n"
        s += "}"
        return s