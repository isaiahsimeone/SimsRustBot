
from __future__ import annotations
import asyncio
from time import time
from typing import TYPE_CHECKING, List

import loguru

from ipc.data_models import CargoDespawned, CargoSpawned, ExplosionExpired, HeliDespawned, HeliDowned, HeliSpawned, RustMapMarkers
from ipc.rust_socket_manager import RustSocketManager

if TYPE_CHECKING:
    pass
import math
from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable
from rustplus import RustSocket

from rustplus.api.structures.rust_marker import RustMarker
from rustplus.api.structures.rust_info import RustInfo
from rustplus.api.structures.rust_map import RustMonument

import random

class MapPollerService(BusSubscriber, Loggable):
    
    OUT_OF_MAP_THRESHOLD = 2000 #TODO: Scale dynamically according to server size
    
    def __init__(self: MapPollerService, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket
        
        self.server_info: RustInfo
        
        self.poll_rate = 999
        
        self.active_helis: dict[int, RustMarker] = {}
        self.active_cargos: dict[int, RustMarker] = {}
        
        # Track explosion marker and its start time
        self.active_explosions: dict[RustMarker, int] = {}
    
    @loguru.logger.catch
    async def execute(self: MapPollerService) -> None:
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = (await RustSocketManager.get_instance()).socket
        # Set map polling frequency
        self.poll_rate = int(self.config["RustPlusAPIService"]["map_polling_frequency"])
        self.explosion_persist_time = 100#int(self.config["RustPlusAPIService"]["explosion_marker_persist_time"])
        # Get server info - RustPlusAPIService publishes this on startup to save tokens
        self.server_info = (await self.last_topic_message_or_wait("server_info")).data["server_info"]
        
        
        message = f"Map marker polling will occur every {self.poll_rate} seconds"
        if self.poll_rate < 5:
            message += "- This is fast, you may be rate limited."
            self.warning(message)
        else:
            self.info(message)
        
        # Map polling loop
        while True:
            await self.poll_markers()
            await asyncio.sleep(self.poll_rate)
            
    async def poll_markers(self) -> None:
        markers: List[RustMarker] = await self.socket.get_markers()
        events: List[RustMarker] = await self.socket.get_current_events()

        # Some events are duplicates of markers, combine the dictionary to remove duplicates
        unique_markers = {m.id: m for m in (markers + events)}.values()
        # Combined
        markers: List[RustMarker] = list(unique_markers)
        
        # Check active heli's. When a heli has gone down since the last poll frame, this will return 
        # an explosion marker ONCE. If multiple heli's go down in the same poll frame, multiple 
        # explosion markers are returned
        explosion_markers = await self.check_helis(markers)
        
        # Track each explosion
        for explosion in explosion_markers:
            self.active_explosions[explosion] = int(time())
        
        # Check if current explosions should be removed
        if self.active_explosions:
            time_now = int(time())
            expired_markers = [marker for marker, start_time in self.active_explosions.items()
                            if time_now > start_time + self.explosion_persist_time]

            for explosion_marker in expired_markers:
                await self.publish("explosion_expired", ExplosionExpired(id=str(explosion_marker.id)))
                del self.active_explosions[explosion_marker]
            markers.extend([marker for marker in self.active_explosions if marker not in expired_markers])

        # Check cargo ships
        await self.check_cargos(markers)
        
        # Publish the markers to the bus
        await self.publish("map_markers", RustMapMarkers(markers=markers))
        

    async def check_helis(self, markers: List[RustMarker]) -> List[RustMarker]:
        heli_markers: List[RustMarker] = self.find_markers_with_type(markers, RustMarker.PatrolHelicopterMarker)
        explosions = []

        self.debug("There are", len(heli_markers), "Helis on the map")
        
        # Collect IDs of helis to be removed
        helis_to_remove = []

        for heli_id, heli in self.active_helis.items():
            if heli not in heli_markers:
                # This heli went down, or left the map
                if self.distance_to_marker(heli) > self.server_info.size * 4:
                    await self.publish("heli_despawned", HeliDespawned(id=str(heli.id)))
                    helis_to_remove.append(heli_id)
                    continue

                # Otherwise, it went down
                await self.publish("heli_downed", HeliDowned(id=str(heli.id), x=heli.x, y=heli.y))

                # Which means it created an explosion. Just use the old marker - we don't need it anymore
                heli._id = random.randint(0, 99999999)  # hopefully no collision
                heli._type = RustMarker.ExplosionMarker
                heli._rotation = 0
                explosions.append(heli)
                helis_to_remove.append(heli_id)

        # Delete helis after iterating
        for heli_id in helis_to_remove:
            del self.active_helis[heli_id]

        # Update heli positions and check for new spawns
        for heli in heli_markers:
            if heli.id not in self.active_helis:
                cardinal_bearing = self.cardinal_bearing_to_marker(heli)
                await self.publish("heli_spawned", HeliSpawned(id=str(heli.id), cardinal_bearing=cardinal_bearing))
            self.active_helis[heli.id] = heli

        return explosions
    
    async def check_cargos(self, markers: List[RustMarker]) -> List[RustMarker] | None:
        cargo_markers = self.find_markers_with_type(markers, RustMarker.CargoShipMarker)
        
        self.debug("There are", len(cargo_markers), "Cargo ships on the map")
        
        for _, cargo in self.active_cargos.items():
            if cargo not in cargo_markers:
                # This cargo left the map
                await self.publish("cargo_despawned", CargoDespawned(id=str(cargo.id)))
                
        for cargo in cargo_markers:
            # A cargo ship just spawned
            if cargo.id not in self.active_cargos:
                cardinal_bearing = self.cardinal_bearing_to_marker(cargo)
                await self.publish("cargo_spawned", CargoSpawned(id=str(cargo.id), cardinal_bearing=cardinal_bearing))
            # Update positions of cargo ships
            self.active_cargos[cargo.id] = cargo
    
    
    def find_markers_with_type(self, markers: List[RustMarker], marker_type: int) -> List[RustMarker]:
        """Find all markers with the specified type, from a list of markers

        :param markers: A list of rust markers to search linearly
        :type markers: List[:class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>]
        :param marker_type: The type of marker to find
        :type marker_type: int
        :return: A list of RustMarkers with the specified type, None otherwise
        :rtype: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker> | None
        """
        return [marker for marker in markers if marker.type == marker_type]

    def bearing_to_marker(self, marker: RustMarker) -> float:
        """Determine the geographic bearing to a provided RustMarker
        from the map origin (map_size / 2, map_size / 2).

        :param marker: The marker
        :type marker: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>
        :return: The geographic bearing to the marker from the map origin (in degrees)
        :rtype: float
        """
        map_center_x = self.server_info.size / 2
        map_center_y = self.server_info.size / 2

        dx = marker.x - map_center_x
        dy = map_center_y - marker.y # Inverted

        angle_radians = math.atan2(dy, dx)

        angle_degrees = math.degrees(angle_radians)

        geographic_bearing = ((angle_degrees + 360) % 360 + 90) % 360

        if geographic_bearing < 0:
            geographic_bearing += 360

        return geographic_bearing


    def distance_to_marker(self, marker: RustMarker) -> float:
        """Determine the distance to a given marker from the
        map origin (map_size / 2, map_size / 2).

        :param marker: The marker to find the distance to
        :type marker: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>
        :return: The pythagorean distance to the marker from the map origin
        :rtype: float
        """
        map_center_x = self.server_info.size / 2
        map_center_y = self.server_info.size / 2
        
        dx = marker.x - map_center_x
        dy = marker.y - map_center_y
        
        return math.sqrt(dx**2 + dy**2)

    def cardinal_bearing_to_marker(self, marker: RustMarker) -> str:
        """Determine the cardinal bearing to the given marker,
        from the map origin (map_size / 2, map_size / 2)

        :param marker: The marker to find the cardinal bearing to
        :type marker: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>
        :return: A string literal: North, North-East, East, South-East, etc
        :rtype: str
        """
        angle = self.bearing_to_marker(marker) # 90 degrees == EAST
        
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
    
    async def on_message(self: MapPollerService, topic: str, message: Message) -> None:
        """Receive a message, under a subscribed topic, from the bus.

        :param self: This instance
        :type self: :class:`MapPollerService <rustplus_api.services.map_poller_service.MapPollerService>`
        :param topic: The topic of the message being received
        :type topic: str
        :param message: The message being received
        :type message: :class:`Message<ipc.message.Message>`
        """
        self.debug(f"Bus message ({topic}):", message)