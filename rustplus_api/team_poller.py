import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.messenger import Service
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object
from util.tools import Tools

class TeamPoller:
    def __init__(self, socket, messenger):
        self.socket = socket
        self.messenger = messenger
        
        self.poll_rate = int(messenger.get_config().get("rust").get("polling_frequency_seconds"))
        
        self.last_team_members_info = None
    
    
    async def start_team_polling(self):
        while True:
            print("poll team")
            await self.poll_team()
            await asyncio.sleep(self.poll_rate)
    
    # Check for changes to team - sends message only if is_online, is_alive, spawn_time, or death_time has changed
    async def poll_team(self):
        team_members_info = serialise_API_object((await self.socket.get_team_info()).members)
        
        if self.last_team_members_info is not None:
            for member in team_members_info:
                steam_id = member["steam_id"]
                
                member_prev = next((m for m in self.last_team_members_info if m['steam_id'] == steam_id), None)
                
                change_type = None
                
                if not member_prev:
                    change_type = "new_team_member"
                    print("SOMEONE JOINED THE TEAM!")
                    return None
                
                if member["is_alive"] != member_prev["is_alive"]:
                    change_type = "player_" + ("spawned" if member["is_alive"] else "died")
                    print(member["name"] + " is " + change_type)
                    
                if member["is_online"] != member_prev["is_online"]:
                    change_type = "player_" + ("online" if member["is_online"] else "offline")
                    print(member["name"] + " is " + change_type)
                    
                if change_type:
                    # SteamID as an integer makes JS play up, convert to string
                    steam_id_int_rep = member_prev.get("steam_id")
                    member_prev["steam_id"] = str(steam_id_int_rep)
                
                    msg_data = {change_type: member_prev} # Send the old entry, so we know where they died approximately
                    message = Message(MessageType.RUST_PLAYER_STATE_CHANGE, msg_data)
                    await self.send_message(message)
                    
        self.last_team_members_info = team_members_info

        
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.messenger.send_message(Service.RUSTAPI, message, target_service_id)