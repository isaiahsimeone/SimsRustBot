from enum import Enum

from ipc.data_models import *

class MessageType(Enum):
    RUST_CHAT_MESSAGE = ("rust_chat_msg", RustTeamChatMessage)
    RUST_TEAM_CHANGE = ("rust_team_change", RustTeamChange)
    
    RUST_SERVER_MAP = ("rust_server_map", RustServerMap)
    RUST_MAP_MARKERS = ("rust_map_markers", RustMapMarkers)
    RUST_MAP_EVENTS = ("rust_map_events", RustMapEvents)
    RUST_MAP_MONUMENTS = ("rust_map_monuments", RustMapMonuments)
    RUST_SERVER_INFO = ("rust_server_info", RustServerInfo)
    RUST_TEAM_INFO = ("rust_team_info", RustTeamInfo)
    RUST_TEAM_CHAT_INIT = ("rust_team_chat_init", RustTeamChatInitial)
    
    # Heli
    RUST_HELI_SPAWNED = ("rust_heli_spawned", RustHeliSpawned)
    RUST_HELI_DOWNED = ("rust_heli_downed", RustHeliDowned)
    RUST_HELI_DESPAWNED = ("rust_heli_despawned", RustHeliDespawned)
    
    # Cargo
    RUST_CARGO_SPAWNED = ("rust_cargo_spawned", RustCargoSpawned)
    RUST_CARGO_DESPAWNED = ("rust_cargo_despawned", RustCargoDespawned)
    
    RUST_PLAYER_STATE_CHANGE = ("rust_player_state_change", RustPlayerStateChange)
    
    # Request
    REQUEST_RUST_SERVER_MAP = ("request_rust_server_map", RustRequestServerMap)
    REQUEST_RUST_MAP_MARKERS = ("request_rust_map_markers", RustRequestMapMarkers)
    REQUEST_RUST_MAP_EVENTS = ("request_rust_map_events", RustRequestMapEvents)
    REQUEST_RUST_MAP_MONUMENTS = ("request_rust_map_monuments", RustRequestMapMonuments)
    REQUEST_RUST_SERVER_INFO = ("request_rust_server_info", RustRequestServerInfo)
    REQUEST_RUST_TEAM_INFO = ("request_rust_team_info", RustRequestTeamInfo)
    REQUEST_RUST_TEAM_CHAT_INIT = ("request_team_chat_init", RustRequestTeamChatInitial)
    REQUEST_ITEM_COUNT = ("request_item_count", RustRequestItemCount)
    REQUEST_SEND_TEAM_MESSAGE = ("request_send_team_message", RustRequestSendTeamMessage)
    # Items
    RUST_ITEM_COUNT = ("rust_item_count", RustItemCount)

    # For the API to do
    #SEND_TEAM_MESSAGE = "send_team_message"
    
    # Devices
    DEVICE_PAIRED = ("device_paired", RustDevicePaired)
    DEVICE_ALARM_MSG = ("device_alarm_msg", RustDeviceAlarmMessage)
    
    TEST = ("test", Test)
    
    def __init__(self, value, model):
        self._value_ = value
        self.model = model