from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ipc.bus import BUS
    from rustplus import ChatEvent, TeamEvent, EntityEvent
    from rustplus_api.rust_plus_api import RustPlusAPI
    
from util.loggable import Loggable
from rustplus import entity_type_to_string
from ipc.bus import Service
from ipc.message import Message, MessageType

from ipc.data_models import RustChatMessage, RustTeamChange, RustTeamChatMessage
class EventListener(Loggable): 
    def __init__(self, rust_api: RustPlusAPI):
        self.api = rust_api
        self.socket = rust_api.get_socket()
        self.BUS = rust_api.get_BUS()
        super().__init__(rust_api.log)
        
        # Register handlers
        self.socket.team_event(self.team_event_handler)
        self.socket.chat_event(self.chat_event_handler)
        self.socket.protobuf_received(self.proto_event_handler)
        #self.socket.entity_event(self.entity_event_handler)
    
    # TODO: may be broken ? Check after FCM listener is sorted
    async def entity_event_handler(self, event: EntityEvent):
        print("EVENT:", event)
        value = "On" if event.value else "Off"
        self.log(f"Entity {event.entity_id} of type {entity_type_to_string(event.type)} has been turned {value}")
        # Additional code to handle entity event

    """
    Rustplus API documentation decorates the callback function
    with #socket.entity_event(ENTITYID), we need to wrap
    """
    def register_entity_event_listener(self, entity_id):
        self.socket.remote.handle_subscribing_entity(entity_id, self.entity_event_handler)
        print("REGISTERED", entity_id)


    def update_smart_switch_handlers(self):
        switch_ids = self.api.BUS.db_query("id", "Devices", "dev_type=1")
        for id in switch_ids:
            self.register_entity_event_listener(id)
        self.log("Switchids:", switch_ids)
        

    async def team_event_handler(self, event: TeamEvent):
        team_info = event.team_info

        data = RustTeamChange(
            leader_steam_id = team_info.leader_steam_id,
            members = team_info.members,
            map_notes = team_info.map_notes,
            leader_map_notes = team_info.leader_map_notes
        )
        
        message = Message(MessageType.RUST_TEAM_CHANGE, data)
        await self.send_message(message)

    async def chat_event_handler(self, event: ChatEvent):
        steam_id = event.message.steam_id
        name = event.message.name
        message = event.message.message
        colour = event.message.colour
        time = event.message.time
        
        # Handle command
        await self.api.execute_command(message, steam_id)
        data = RustTeamChatMessage(steam_id=steam_id, name=name, message=message, colour=colour, time=time)
        message = Message(MessageType.RUST_CHAT_MESSAGE, data)
        await self.send_message(message)
        
    async def proto_event_handler(self, data: bytes):
        pass
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)
    