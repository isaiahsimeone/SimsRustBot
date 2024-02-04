import asyncio
from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string
from ipc.messenger import Service
from ipc.message import Message, MessageType

class EventListener: 
    def __init__(self, socket, messenger):
        self.socket = socket
        self.messenger = messenger
        
        #ALARM LISTENER HERE
        self.socket.team_event(self.team_event_handler)
        self.socket.chat_event(self.chat_event_handler)
        self.socket.protobuf_received(self.proto_event_handler)
        
    async def alarm(self, event : EntityEvent):
        value = "On" if event.value else "Off"
        print(f"{entity_type_to_string(event.type)} has been turned {value}")

    async def team_event_handler(self, event: TeamEvent):
        print("TEAM EVENT" + event.team_info.__dir__())
        team_info = event.team_info
        msg_data = {"leader_steam_id": team_info.leader_steam_id, "members": str(team_info.members), "map_notes": str(team_info.map_notes), "leader_map_notes:": str(team_info.leader_map_notes)}
        message = Message(MessageType.RUST_TEAM_CHANGE, msg_data)
        self.send_message(message)
        print(f"The team leader's steamId is: {event.team_info.leader_steam_id}")

    async def chat_event_handler(self, event: ChatEvent):
        print("CHAT EVENT" + event.team_info.__dir__())
        msg_data = {"name": event.message.name, "msg": event.message.message}
        message = Message(MessageType.RUST_IN_GAME_MSG, msg_data)
        #self.send_message(message)
        print("chat handled")
        
    async def proto_event_handler(self, data: bytes):
        print("PROTO EVENT" + event.team_info.__dir__())
        #print(data)
        pass
        
    def send_message(self, message: Message, target_service_id=None):
        self.messenger.send_message(Service.RUSTAPI, message, target_service_id)
    