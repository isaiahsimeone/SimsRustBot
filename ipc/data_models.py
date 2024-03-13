
from pydantic import BaseModel as PydanticBaseModel
from typing import Any, List, Dict, Optional

from rustplus.api.structures.rust_team_info import RustTeamMember, RustTeamNote
from rustplus.api.structures.rust_marker import RustColour, RustSellOrder, RustMarker
from rustplus.api.structures.rust_info import RustInfo
from rustplus.api.structures.rust_map import RustMonument, RustMap
from rustplus.api.structures.rust_chat_message import RustChatMessage #type:ignore
from rustplus.api.structures.rust_contents import RustContents
from rustplus.api.structures.rust_item import RustItem

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class RustTeamChatMessage(BaseModel):
    steam_id: int
    name: str
    message: str
    colour: str
    time: int
    
class RustTeamChange(BaseModel):
    leader_steam_id: int
    members: List[RustTeamMember]
    map_notes: List[RustTeamNote]
    leader_map_notes: List[RustTeamNote]
    
class RustServerMap(BaseModel):
    width: int
    height: int
    pixels: str # base64 encoded on bus

class RustMapMarkers(BaseModel):
    markers: List[Any]

class RustMapEvents(BaseModel):
    pass

class RustMapMonuments(BaseModel):
    monuments: List[RustMonument]
    background: str

class RustServerInfo(BaseModel):
    url: str
    name: str
    map: str
    size: int
    players: int
    max_players: int
    queued_players: int
    seed: int
    wipe_time: int
    header_image: str
    logo_image: str

class RustTeamInfo(BaseModel):
    leader_steam_id: int
    members: List[RustTeamMember]
    map_notes: List[RustTeamNote]
    leader_map_notes: List[RustTeamNote]

class RustTeamChatInitial(BaseModel):
    chats: List[RustChatMessage]

class RustHeliSpawned(BaseModel):
    bearing: str

class RustHeliDowned(BaseModel):
    position: Dict[str, int]

class RustHeliDespawned(BaseModel):
    pass

class RustCargoSpawned(BaseModel):
    bearing: str

class RustCargoDespawned(BaseModel):
    pass

class RustPlayerStateChange(BaseModel):
    pass

class RustRequestMapMarkers(BaseModel):
    pass

class RustRequestMapMonuments(BaseModel):
    pass

class RustRequestMapEvents(BaseModel):
    pass

class RustRequestServerMap(BaseModel):
    pass

class RustRequestServerInfo(BaseModel):
    pass

class RustRequestTeamInfo(BaseModel):
    pass

class RustRequestTeamChatInitial(BaseModel):
    pass

class RustRequestItemCount(BaseModel):
    pass

class RustRequestSendTeamMessage(BaseModel):
    steam_id: int
    name: Optional[str] = None
    message: str
    time: Optional[int] = -1




class RustItemCount(BaseModel):
    pass

class RustDevicePaired(BaseModel):
    id: str
    name: str
    dev_type: int
    state: bool

class RustDeviceAlarmMessage(BaseModel):
    title: str
    message: str

class Test(BaseModel):
    content: str

