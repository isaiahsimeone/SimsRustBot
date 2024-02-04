import asyncio
from rustplus import RustSocket, ChatEvent, TeamEvent, EntityEvent, entity_type_to_string

async def alarm(event : EntityEvent):
  value = "On" if event.value else "Off"
  print(f"{entity_type_to_string(event.type)} has been turned {value}")

async def team_event_handler(event: TeamEvent):
    print(f"The team leader's steamId is: {event.team_info.leader_steam_id}")

async def chat_event_handler(event: ChatEvent):
    print(f"{event.message.name}: {event.message.message}")

async def proto_event_handler(data: bytes):
    print(data)