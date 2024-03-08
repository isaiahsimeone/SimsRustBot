from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipc.bus import BUS
    from rustplus_api.rust_plus_api import RustPlusAPI

import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.bus import Service
from ipc.data_models import RustTeamChange
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object
from util.tools import Tools
import json
import copy

from util.loggable import Loggable

class TeamPoller(Loggable):
    def __init__(self, rust_api: RustPlusAPI):
        self.api = rust_api
        self.BUS = rust_api.get_BUS()
        super().__init__(rust_api.log)
        
        self.poll_rate = int(self.BUS.get_config().get("rust").get("polling_frequency_seconds"))
        
        self.last_team_info_hash = None
    
    
    async def start_team_polling(self):
        while True:
            self.log("poll team")
            await self.poll_team()
            await asyncio.sleep(self.poll_rate)
    
    # Check for changes to team - sends message only if is_online, is_alive, spawn_time, or death_time has changed
    async def poll_team(self):
        team_info = await self.api.get_socket().get_team_info()
        
        new_hash = self.hash_team_info(team_info)
        
        if self.last_team_info_hash is not None:
            if self.last_team_info_hash != new_hash:
                # The team has changed (excluding a team members coordinates, spawn, or death time)
                self.log("Team changed")

                data = RustTeamChange(
                    leader_steam_id=team_info.leader_steam_id,
                    members=team_info.members,
                    map_notes=team_info.map_notes,
                    leader_map_notes=team_info.leader_map_notes
                )
                
                message = Message(MessageType.RUST_TEAM_INFO, data)
                await self.send_message(message)
            
        self.last_team_info_hash = new_hash
        
    def hash_team_info(self, team_info_now):
        # Deepcopy so attributes deleted here remain in parents scope
        team_info = serialise_API_object(copy.deepcopy(team_info_now))
        # We don't care about these things changing
        for i in range(0, len(team_info['members'])):
            del team_info['members'][i]['x']    
            del team_info['members'][i]['y']    
            del team_info['members'][i]['spawn_time']    
            del team_info['members'][i]['death_time']
        
        return hash(json.dumps(team_info))       
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)