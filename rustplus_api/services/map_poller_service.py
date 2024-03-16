
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, List

import loguru

from ipc.data_models import RustCargoDespawned, RustCargoSpawned, RustHeliDespawned, RustHeliDowned, RustHeliSpawned, RustMapMarkers
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
from rustplus.api.remote.rustplus_proto import AppMarker

class MapPollerService(BusSubscriber, Loggable):
    
    OUT_OF_MAP_THRESHOLD = 2000 #TODO: Scale dynamically according to server size
    
    def __init__(self: MapPollerService, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocket
        
        self.server_info: RustInfo
        
        self.poll_rate = 999
        self.cargo_is_out = False
        self.heli_is_out = False
        self.last_heli_marker: RustMarker
    
    @loguru.logger.catch
    async def execute(self: MapPollerService) -> None:
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = (await RustSocketManager.get_instance()).socket
        # Set map polling frequency
        self.poll_rate = int(self.config["RustPlusAPIService"]["polling_frequency_seconds"])
        # Get server info - RustPlusAPIService publishes this on startup to save tokens
        self.server_info = (await self.last_topic_message_or_wait("server_info")).data["server_info"]
        
        message = f"Map markers will be polled every {self.poll_rate} seconds"
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
        
        # Check for heli
        explosion_marker = await self.check_for_heli(markers)
        if explosion_marker:
           markers.append(explosion_marker)
           
        # Check for cargo
        await self.check_for_cargo(markers)
        
        # Publish the markers to the bus
        await self.publish("map_markers", Message(RustMapMarkers(markers=markers)))

    # Can only handle one heli out at a time
    async def check_for_heli(self, markers: List[RustMarker]) -> RustMarker | None:
        """Determine whether the PatrolHelicopter spawns, gets taken down or despawns, and
        publishes these events to the :class:`MessageBus <ipc.message_bus.MessageBus>`
        
        For this functionality to work properly, there can only be one patrol helicopter
        on the map at a time.

        :param markers: A list of rust markers (from rustplus.py `get_markers` and `get_current_events` combined)
                        To search through for a PatrolHelicopter marker
        :type markers: List[RustMarker]
        :return: A :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker> to an active heli, or None
        :rtype: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker> | None
        """
        heli_marker: RustMarker | None = self.find_marker_with_type(markers, RustMarker.PatrolHelicopterMarker)
        
        # Heli went down, or left the map
        if self.heli_is_out and not heli_marker:
            self.heli_is_out = False
            
            # If heli is 4 * the map size away, it's probably leaving
            if self.distance_to_marker(self.last_heli_marker) > self.server_info.size * 4:
                await self.publish("heli", Message(RustHeliDespawned()))
                return None

            # Otherwise, heli was downed
            # Publish under heli topic that heli went down
            model = RustHeliDowned(x=self.last_heli_marker.x, y=self.last_heli_marker.y)
            await self.publish("heli", Message(model))
            
            # Just use the old marker - we don't need it anymore
            self.last_heli_marker._type = RustMarker.ExplosionMarker
            self.last_heli_marker._rotation = 0
            explosion_marker = self.last_heli_marker
            
            return explosion_marker
        
        # Heli has just entered the map
        if not self.heli_is_out and heli_marker:
            self.heli_is_out = True
            
            cardinal_bearing = self.cardinal_bearing_to_marker(heli_marker)
            
            await self.publish("heli", Message(RustHeliSpawned(cardinal_bearing=cardinal_bearing)))
            
            #TODO: This needs to get to the gamechat
            
        if self.heli_is_out and heli_marker:
            self.last_heli_marker = heli_marker
            self.debug("Update heli position")
            
    # Can only handle one cargo at a time
    async def check_for_cargo(self, markers: List[RustMarker]) -> None:
        """Determine whether the CargoShip spawns or despawns, and
        publishes these events to the :class:`MessageBus <ipc.message_bus.MessageBus>`

        :param markers: A list of rust markers (from rustplus.py `get_markers` and `get_current_events` combined)
        :type markers: List[:class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>]
        :return: Nothing
        :rtype: None
        """
        cargo_marker = self.find_marker_with_type(markers, RustMarker.CargoShipMarker)
        
        # Cargo left the map
        if self.cargo_is_out and not cargo_marker:
            self.cargo_is_out = False
            await self.publish("cargo", Message(RustCargoDespawned()))
            return None
        
        # Cargo is now out
        if not self.cargo_is_out and cargo_marker:
            self.cargo_is_out = True
            
            cardinal_bearing = self.cardinal_bearing_to_marker(cargo_marker)
            
            await self.publish("cargo", Message(RustCargoSpawned(cardinal_bearing=cardinal_bearing)))
    
    def find_marker_with_type(self, markers: List[RustMarker], marker_type: int) -> RustMarker | None:
        """Find a marker with the specified type, from a list of markers

        :param markers: A list of rust markers to search linearly
        :type markers: List[:class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker>]
        :param marker_type: The type of marker to find
        :type marker_type: int
        :return: The first marker in the list with the specified type, None otherwise
        :rtype: :class:`RustMarker <rustplus.api.structures.rust_marker.RustMarker> | None
        """
        for marker in markers:
            if marker.type == marker_type:
                return marker
        return None

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