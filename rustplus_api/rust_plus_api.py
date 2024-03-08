from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ipc.bus import BUS

from ipc.bus import Service
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object

from rustplus import RustSocket
import asyncio
from .FCM_listener import FCM
from .map_poller import MapPoller
from .team_poller import TeamPoller
from .event_listener import EventListener

from .message_executor import MessageExecutor

from .storage_monitor_manager import StorageMonitorManager

from .rust_item_name_manager import RustItemNameManager

from rustplus_api.commands.command_executor import CommandExecutor



import json

class RustPlusAPI():
    def __init__(self, BUS: BUS):
        self.BUS = BUS
        self.config = BUS.get_config()
        self.server = self.config.get("server_details").get("ip")
        self.port = self.config.get("server_details").get("port")
        self.steamID = self.config.get("server_details").get("playerId")
        self.playerToken = self.config.get("server_details").get("playerToken")
        self.socket = RustSocket(self.server, self.port, self.steamID, self.playerToken)
        self.command_executor = CommandExecutor(self, self.config.get("rust").get("command_prefix"))
        self.event_listener = None
        self.server_info = None
        self.rust_item_name_manager = RustItemNameManager()
        self.storage_monitor_manager = StorageMonitorManager(self, self.rust_item_name_manager)
        
    # entry point
    def execute(self):
        asyncio.run(self.api_main())

    async def api_main(self):
        self.log("Connecting to Rust Server (" + self.server + ")...")
        await self.socket.connect()
        self.log("Connected to Rust Server! (" + self.server + ")")

        self.executor = MessageExecutor(self)
        self.BUS.subscribe(Service.RUSTAPI, self.process_message)
        self.log("Rust Service subscribed for messages")
        
        self.log("Starting FCM listener...")
        self.fcm = FCM(self.config.get("fcm_credentials"), self).start()
        self.log("FCM Listener startup complete")

        self.log("Fetching server info...")
        #self.log("Downloading server map...")

        # Name manager for items - loads aliases etc

        # Register event listener
        self.event_listener = EventListener(self)
        self.log("Event listener setup complete")
        
        
        self.map_poller = MapPoller(self)
        self.team_poller = TeamPoller(self)
        
        #self.storage_monitor_manager.get_monitor_ids()
        
        self.server_info = serialise_API_object(await self.socket.get_info())
        
        #DEBUG
        self.log("Got Server Info: " + str(self.server_info))
        
        # Start map marker polling
        asyncio.create_task(self.map_poller.start_marker_polling(self.server_info)) # TODO: pass this into the constructor, not here
    
        # Start team polling
        asyncio.create_task(self.team_poller.start_team_polling())
        

        poll_rate_map_team = self.BUS.get_config().get("rust").get("polling_frequency_seconds")
        self.log("Map marker and team polling started with a frequency of " + poll_rate_map_team + " seconds")
        
        should_poll_storage = self.BUS.get_config().get("rust").get("storage_monitor_should_poll")
        if should_poll_storage:
            poll_rate_storage = self.BUS.get_config().get("rust").get("storage_monitor_polling_frequency_seconds")
            # Storage monitor polling
            asyncio.create_task(self.storage_monitor_manager.start_storage_polling())
            self.log("Storage Monitor polling started with a frequency of " + poll_rate_storage + " seconds")
         
        await asyncio.Future() # Keep running
        
        self.log("asyncio.Future() finished? Exiting", type="error")

    
    def get_socket(self):
        return self.socket
    
    def get_BUS(self):
        return self.BUS
    
    def get_config(self):
        return self.config
    
    async def send_game_message(self, message, sender=None):
        author = ""
        if sender:
            author = f"[{sender}]"
        await self.socket.send_team_message("[BOT] " + str(author) + " " + str(message))
        
    async def execute_command(self, command_string, sender_steam_id):
        res = await self.command_executor.parse_and_execute_command(command_string, sender_steam_id)
        if res and res[0] == '?':
            components = res.split(':')
            await self.send_game_message(f"Unknown command '{components[1]}'. Did you mean '{components[2]}'?")

    async def disconnect_api(self):
        self.log("Disconnecting from Rust Server (" + self.server + ")...")
        await self.socket.disconnect()
        self.log("Disconnected from Rust Server (" + self.server + ")")

    async def process_message(self, msg, sender):
        msg = json.loads(msg)
        await self.executor.execute_message(msg, sender)

    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)

    def log(self, *args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        log_type = kwargs.get("type", "info")
        self.BUS.log(Service.RUSTAPI, message, type=log_type)
