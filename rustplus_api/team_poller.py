import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.bus import Service
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object
from util.tools import Tools
import json
import copy

class TeamPoller:
    def __init__(self, socket, BUS):
        self.socket = socket
        self.BUS = BUS
        
        self.poll_rate = int(BUS.get_config().get("rust").get("polling_frequency_seconds"))
        
        self.last_team_info_hash = None
    
    
    async def start_team_polling(self):
        while True:
            print("poll team")
            await self.poll_team()
            await asyncio.sleep(self.poll_rate)
    
    # Check for changes to team - sends message only if is_online, is_alive, spawn_time, or death_time has changed
    async def poll_team(self):
        team_info = serialise_API_object((await self.socket.get_team_info()))
        
        new_hash = self.hash_team_info(team_info)
        
        if self.last_team_info_hash is not None:
            if self.last_team_info_hash != new_hash:
                # The team has changed (excluding a team members coordinates, spawn, or death time)
                print("Team changed")
                message = Message(MessageType.RUST_TEAM_INFO, {"data": team_info})
                await self.send_message(message)
            
        self.last_team_info_hash = new_hash
        
    def hash_team_info(self, team_info_now):
        # Deepcopy so attributes deleted here remain in parents scope
        team_info = copy.deepcopy(team_info_now)
        # We don't care about these things changing
        for i in range(0, len(team_info['members'])):
            del team_info['members'][i]['x']    
            del team_info['members'][i]['y']    
            del team_info['members'][i]['spawn_time']    
            del team_info['members'][i]['death_time']
        
        return hash(json.dumps(team_info))
    
        """
        if self.last_team_members_info is not None:
            for member in team_members_info:
                steam_id = member["steam_id"]
                
                member_prev = next((m for m in self.last_team_members_info if m['steam_id'] == steam_id), None)
                
                change_type = None
                
                if not member_prev:
                    change_type = "new_team_member"
                    print("Someone joined the team")
                    return None
                
                if member["is_alive"] != member_prev["is_alive"]:
                    change_type = "player_" + ("spawned" if member["is_alive"] else "died")
                    print(member["name"] + " is " + change_type)
                    
                if member["is_online"] != member_prev["is_online"]:
                    change_type = "player_" + ("online" if member["is_online"] else "offline")
                    print(member["name"] + " is " + change_type)
                    
                if change_type:
                    message = Message(MessageType.RUST_TEAM_INFO, {"data": self.team_members_info})
                    await self.send_message(message)
                    
        self.last_team_members_info = team_members_info
        """
        
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)