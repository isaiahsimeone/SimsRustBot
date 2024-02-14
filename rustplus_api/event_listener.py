import asyncio
from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.bus import Service
from ipc.message import Message, MessageType

class EventListener: 
    def __init__(self, socket, BUS):
        self.socket = socket
        self.BUS = BUS
        
        # Register handlers
        self.socket.team_event(self.team_event_handler)
        self.socket.chat_event(self.chat_event_handler)
        self.socket.protobuf_received(self.proto_event_handler)
        self.socket.entity_event(self.entity_event_handler)
    
    # TODO: may be broken ? Check after FCM listener is sorted
    async def entity_event_handler(self, event : EntityEvent):
        value = "On" if event.value else "Off"
        print(f"Entity {event.entity_id} of type {entity_type_to_string(event.type)} has been turned {value}")
        # Additional code to handle entity event

    # TODO: mightn't need to get map notes, they might be retrievable from map marker polling
    async def team_event_handler(self, event: TeamEvent):
        team_info = event.team_info
        msg_data = {"leader_steam_id": team_info.leader_steam_id, 
                    "members": team_info.members, 
                    "map_notes": team_info.map_notes, 
                    "leader_map_notes:": team_info.leader_map_notes}
        
        message = Message(MessageType.RUST_TEAM_CHANGE, msg_data)
        await self.send_message(message)
        #print(f"The team leader's steamId is: {event.team_info.leader_steam_id}")

    async def chat_event_handler(self, event: ChatEvent):
        msg_data = {"steam_id": event.message.steam_id, 
                    "name": event.message.name, 
                    "msg": event.message.message,
                    "colour": event.message.colour,
                    "time": event.message.time}
        message = Message(MessageType.RUST_IN_GAME_MSG, msg_data)
        await self.send_message(message)
        
    async def proto_event_handler(self, data: bytes):
        pass
        
    async def send_message(self, message: Message, target_service_id=None):
        await self.BUS.send_message(Service.RUSTAPI, message, target_service_id)
    