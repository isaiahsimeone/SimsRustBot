import asyncio
import rustplus
#from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.bus import Service
from ipc.message import Message, MessageType
from ipc.serialiser import serialise_API_object
from util.tools import Tools
import math
from .commands.send_message import send_message as rust_api_send_message
import random
import time

class MapPoller:
    def __init__(self, socket, BUS):
        self.socket = socket
        self.BUS = BUS
        
        self.poll_rate = int(BUS.get_config().get("rust").get("polling_frequency_seconds"))

        self.heli_is_out = False
        self.last_heli_position = None
        
        self.injected_map_markers = []
    
    async def start_marker_polling(self, server_info):
        self.server_info = server_info
        while True:
            await self.poll_markers()
            await asyncio.sleep(self.poll_rate)
    
    async def poll_markers(self):
        markers = serialise_API_object(await self.socket.get_markers())
        
        updated_injects = []
        for meta, marker in self.injected_map_markers:
            if time.time() < meta['created'] + meta['persist_for']:
                markers.append(marker)
                updated_injects.append((meta, marker))
        
        # Updated to remove expired markers
        self.injected_map_markers = updated_injects
        
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
    
        # Check if heli is out
        await self.check_for_heli(markers)
        
        
        msg_data = {"markers": markers}
        message = Message(MessageType.RUST_MAP_MARKERS, msg_data)
        await self.send_message(message)
    
    # Assumes there's only ever one attack heli on the map
    async def check_for_heli(self, markers):
        heli_marker = self.find_marker_with_type(markers, 8)
        
        
        # heli went down, or despawned
        if self.heli_is_out and not heli_marker:
            self.heli_is_out = False
            
            if self.get_angle_to_marker(heli_marker) > self.server_info['size'] * 6:
                # Probably despawned
                await self.send_message(Message(MessageType.RUST_HELI_DESPAWNED, {}))
                return None
            
            # Otherwise, probably was downed in the map
            await self.send_message(Message(MessageType.RUST_HELI_DOWNED, {"position": self.last_heli_position}))

            marker = {'id': random.randint(0, 10000000), 'x': self.last_heli_position['x'], 'y': self.last_heli_position['y'], 'type': 2}
            meta = {'created': time.time(), 'persist_for': 60 * 15} # marker lasts for 15 minutes
            self.injected_map_markers.append((meta, marker))
        
        # heli is now out
        if not self.heli_is_out and heli_marker:
            print("HELI SPAWNED -- poller")
            self.heli_is_out = True
            await self.send_message(Message(MessageType.RUST_HELI_SPAWNED, {"bearing": self.get_cardinal_bearing(heli_marker)}))
            await rust_api_send_message(self.socket, "Heli just spawned! It will enter the map from the " + str(self.get_cardinal_bearing(heli_marker)))
            
        if self.heli_is_out and heli_marker:
            self.last_heli_position = {'x': heli_marker['x'], 'y': heli_marker['y']}
            print("update heli position", str(self.last_heli_position), str(self.get_cardinal_bearing(heli_marker)))
        
    
    # Returns a string (north, east, south, west, northeast, southeast, northwest, southwest)
    # indicating the bearing of a marker from the center of the map 
    def get_angle_to_marker(self, marker):
               
        map_center_x = self.server_info['size'] / 2
        map_center_y = self.server_info['size'] / 2
        
        dx = marker['x'] - map_center_x
        dy = map_center_y - marker['y'] # Inverted
        
        angle_radians = math.atan2(dy, dx)
        
        angle_degrees = math.degrees(angle_radians)
        
        geographic_bearing = ((angle_degrees + 360) % 360 + 90) % 360
        
        if geographic_bearing < 0:
            geographic_bearing += 360

        return geographic_bearing
    
    def get_cardinal_bearing(self, marker):
        angle = self.get_angle_to_marker(marker) # 90 degrees == EAST
        
        angle %= 360
        
        if 337.5 <= angle or angle < 22.5:
            return 'North'
        elif 22.5 <= angle < 67.5:
            return 'North-East'
        elif 67.5 <= angle < 112.5:
            return 'East'
        elif 112.5 <= angle < 157.5:
            return 'South-East'
        elif 157.5 <= angle < 202.5:
            return 'South'
        elif 202.5 <= angle < 247.5:
            return 'South-West'
        elif 247.5 <= angle < 292.5:
            return 'West'
        elif 292.5 <= angle < 337.5:
            return 'North-West'
        return 'wtf?'
    
    # Return the pythagorean distance to a marker from origin
    def distance_to_marker(self, marker):
        map_center_x = self.server_info['size'] / 2
        map_center_y = self.server_info['size'] / 2
        
        dx = marker['x'] - map_center_x
        dy = marker['y'] - map_center_y
        
        distance = math.sqrt(dx**2 + dy**2)
        
        return distance
    
    # Is a marker with the target type on the map?
    def find_marker_with_type(self, markers, target_type):
        for marker in markers:
            if marker['type'] == target_type:
                return marker
        return None
    
    
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)