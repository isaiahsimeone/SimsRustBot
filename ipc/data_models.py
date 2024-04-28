
import typing
from pydantic import BaseModel as PydanticBaseModel
from typing import Any, List, Dict, Optional

from rustplus.api.structures.rust_team_info import RustTeamMember, RustTeamNote
from rustplus.api.structures.rust_marker import RustColour, RustSellOrder, RustMarker
from rustplus.api.structures.rust_info import RustInfo
from rustplus.api.structures.rust_map import RustMonument, RustMap
from rustplus.api.structures.rust_chat_message import RustChatMessage
from rustplus.api.structures.rust_contents import RustContents
from rustplus.api.structures.rust_item import RustItem
from rustplus.api.structures.rust_team_info import RustTeamInfo

from rustplus import RustSocket

from database.models import ServerToken
from rust_socket.structures.extended_rust_team_note import ExtendedRustTeamNote

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
        
    @property
    def type(self) -> str:
        return self.__class__.__name__

class RustTeamChatMessage(BaseModel):
    steam_id: str
    name: str
    message: str
    colour: str
    time: int
    
class RustTeamChange(BaseModel):
    leader_steam_id: str
    members: List[RustTeamMember]
    map_notes: List[RustTeamNote]
    leader_map_notes: List[RustTeamNote]
    
class RustServerMap(BaseModel):
    width: int
    height: int
    pixels: str # base64 encoded on bus

class RustMapMarkers(BaseModel):
    markers: List[RustMarker]

class RustMonuments(BaseModel):
    monuments: List[RustMonument]
    
class RustBackground(BaseModel):
    background: str

class RustServerInfo(BaseModel):
    server_info: RustInfo

class TeamInfo(BaseModel):
    team_info: RustTeamInfo

class TeamMapNotes(BaseModel):
    map_notes: List[ExtendedRustTeamNote]

class TeamLeft(BaseModel):
    pass

class TeamJoined(BaseModel):
    pass

class TeamLeaderChange(BaseModel):
    new_leader_steam_id: int
    
class TeamMemberJoin(BaseModel):
    member: RustTeamMember

class TeamMemberLeft(BaseModel):
    member: RustTeamMember
    
class TeamMemberConnectivity(BaseModel):
    steam_id: str
    is_online: bool
    
class TeamMemberVital(BaseModel):
    steam_id: str
    is_alive: bool

class RustTeamChatInitial(BaseModel):
    chats: List[RustChatMessage]

class HeliSpawned(BaseModel):
    """The Rust Marker Id of the heli"""
    id: str
    """The cardinal bearing (from the map center) to where heli has entered the map """
    cardinal_bearing: str

class HeliDowned(BaseModel):
    """The Rust Marker Id of the heli"""
    id: str
    """The x-coordinate of where Heli went down"""
    x: float
    """The y-coordinate of where Heli went down"""
    y: float
    """The square on the grid of where Heli went down (e.g. D4)"""
    square: str = '00'   

class HeliDespawned(BaseModel):
    """The Rust Marker Id of the heli"""
    id: str

class ChinookSpawned(BaseModel):
    """The Rust Marker Id of the chinook"""
    id: str
    """The cardinal bearing (from the map center) to where chinook has entered the map """
    cardinal_bearing: str

class ChinookDowned(BaseModel):
    """The Rust Marker Id of the chinook"""
    id: str
    """The x-coordinate of where chinook went down"""
    x: float
    """The y-coordinate of where chinook went down"""
    y: float
    """The square on the grid of where chinook went down (e.g. D4)"""
    square: str

class ChinookDespawned(BaseModel):
    """The Rust Marker Id of the chinook"""
    id: str

class ExplosionMarker(BaseModel):
    """The Rust Marker Id of the explosion"""
    id: str
    """The x-coordinate of the explosion"""
    x: float
    """The y-coordinate of the explosion"""
    y: float

class MarkerExpired(BaseModel):
    """The Rust Marker id of the Marker"""
    id: str

class EventStartTimes(BaseModel):
    """Marker ID to time it spawned"""
    start_times: dict[str, int]

class CargoSpawned(BaseModel):
    """The Rust Marker Id of cargo"""
    id: str
    """The cardinal bearing (from the map center) to where cargo has entered the map """
    cardinal_bearing: str

class CargoDespawned(BaseModel):
    """The Rust Marker Id of cargo"""
    id: str

class PlayerFcmToken(BaseModel): 
    """The steam Id that owns this FCM token"""
    steam_id: str
    """The FCM token"""
    token: str

class PlayerServerToken(BaseModel):
    """The server token"""
    desc: str
    id: str
    img: str
    ip: str
    logo: str
    name: str
    steam_id: str
    playerToken: str
    port: str
    type_: str
    url: str
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    @classmethod
    @typing.no_type_check
    def from_database_server_token(cls, server_token: ServerToken):
        return cls(
            # We are assigning Column[str]. At runtime, these hold a string
            # The type checker can't tell
            desc=server_token.desc,
            id=server_token.id,
            img=server_token.img,
            ip=server_token.ip,
            logo=server_token.logo,
            name=server_token.name,
            steam_id=server_token.steam_id,
            playerToken=server_token.playerToken,
            port=server_token.port,
            type_=server_token.type_,
            url=server_token.url
        )
        
    
class DatabasePlayerServerTokens(BaseModel):
    tokens: List[PlayerServerToken]

class RustPlayerStateChange(BaseModel):
    pass


class RustRequestSendTeamMessage(BaseModel):
    steam_id: str
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
    


class RustServerChanged(BaseModel):
    """The model that is sent when we are connecting to a 
    new server
    """
    pass

class Config(BaseModel):
    """A dictionary containing the configuration information 
    (config.json, fcm and server json files)
    """
    config: Dict
    
class ConfigFileChanged(BaseModel):
    config: Dict[str, Dict[str, str]]

class Test(BaseModel):
    """A model that is used for IPC development testing
    """
    content: str


class Empty(BaseModel):
    pass
