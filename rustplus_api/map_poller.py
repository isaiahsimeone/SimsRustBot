import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.bus import Service
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object
from util.tools import Tools

class MapPoller:
    def __init__(self, socket, BUS):
        self.socket = socket
        self.BUS = BUS
        
        self.poll_rate = int(BUS.get_config().get("rust").get("polling_frequency_seconds"))
    
    
    async def start_marker_polling(self):
        while True:
            await self.poll_markers()
            await asyncio.sleep(self.poll_rate)
    
    async def poll_markers(self):
        markers = serialise_API_object(await self.socket.get_markers())
        events = serialise_API_object(await self.socket.get_current_events())
        
        # Some events are already captured by markers (e.g. Heli), only add missing ones
        marker_ids = [marker.get("id") for marker in markers]
        
        for marker in events:
            if marker.get("id") not in marker_ids:
                markers.add(marker)
        
        # SteamID as an integer makes JS play up, convert to string
        for marker in markers:
            steam_id_int_rep = marker.get("steam_id")
            marker["steam_id"] = str(steam_id_int_rep)
        
        msg_data = {"markers": markers}
        message = Message(MessageType.RUST_MAP_MARKERS, msg_data)
        await self.send_message(message)
        
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)