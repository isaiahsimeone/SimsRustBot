from typing import Any
from rustplus.api.structures.rust_team_info import RustTeamMember, RustTeamNote, RustTeamInfo
from rustplus.api.structures.rust_marker import RustColour, RustSellOrder, RustMarker
from rustplus.api.structures.rust_info import RustInfo
from rustplus.api.structures.rust_map import RustMonument, RustMap
from rustplus.api.structures.rust_chat_message import RustChatMessage
from rustplus.api.structures.rust_contents import RustContents
from rustplus.api.structures.rust_item import RustItem

class_mappings = {
    RustTeamMember: ['steam_id', 'name', 'x', 'y', 'is_online', 'spawn_time', 'is_alive', 'death_time'],
    RustTeamNote: ['type', 'x', 'y', 'icon', 'colour_index', 'label'],
    RustTeamInfo: ['leader_steam_id', 'members', 'map_notes', 'leader_map_notes'],
    RustColour: ['x', 'y', 'z', 'w'],
    RustSellOrder: ['item_id', 'quantity', 'currency_id', 'cost_per_item', 'item_is_blueprint', 'currency_is_blueprint', 'amount_in_stock'],
    RustMarker: ['id', 'type', 'x', 'y', 'steam_id', 'rotation', 'radius', 'colour1', 'colour2', 'alpha', 'name', 'sell_orders', 'out_of_stock'],
    RustInfo: ['url', 'name', 'map', 'size', 'players', 'max_players', 'queued_players', 'seed', 'wipe_time', 'header_image', 'logo_image'],
    RustMap: ['width', 'height', 'margin', 'monuments', 'background'], #TODO: what is background? - omitted jpg_image bc bytes not serialisable
    RustMonument: ['token', 'x', 'y'],
    RustChatMessage: ['steam_id', 'name', 'message', 'colour', 'time'],
    RustContents: ['protection_time', 'has_protection', 'contents'],
    RustItem: ['name', 'item_id', 'quantity', 'is_blueprint']
    
}


def serialise_API_object(obj) -> Any:
    # If the object has a 'serialize' method, use it directly.
    if hasattr(obj, 'serialize') and callable(getattr(obj, 'serialize')):
        return obj.serialize()
    elif isinstance(obj, list):
        # If the object is a list, recursively serialize each item in the list.
        return [serialise_API_object(item) for item in obj]
    else:
        # For basic types that do not need serialization, return the object itself.
        return obj






