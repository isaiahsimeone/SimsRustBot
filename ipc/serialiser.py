import json
from enum import Enum, auto
from rustplus.api.structures.rust_team_info import RustTeamMember, RustTeamNote, RustTeamInfo
from rustplus.api.structures.rust_marker import RustColour, RustSellOrder, RustMarker

class_mappings = {
    RustTeamMember: ['steam_id', 'name', 'x', 'y', 'is_online', 'spawn_time', 'is_alive', 'death_time'],
    RustTeamNote: ['type', 'x', 'y', 'icon', 'colour_index', 'label'],
    RustTeamInfo: ['leader_steam_id', 'members', 'map_notes', 'leader_map_notes'],
    RustColour: ['x', 'y', 'z', 'w'],
    RustSellOrder: ['item_id', 'quantity', 'currency_id', 'cost_per_item', 'item_is_blueprint', 'currency_is_blueprint', 'amount_in_stock'],
    RustMarker: ['id', 'type', 'x', 'y', 'steam_id', 'rotation', 'radius', 'colour1', 'colour2', 'alpha', 'name', 'sell_orders', 'out_of_stock']
}


def serialise_API_object(obj):
    obj_type = type(obj)
    #print(f"Serialising object of type: {obj_type.__name__}")

    if obj_type in class_mappings:
        serialized_data = {}
        for attr in class_mappings[obj_type]:
            attr_value = getattr(obj, attr)
            #print(f"Serializing attribute {attr} of type: {type(attr_value).__name__}")
            serialized_data[attr] = serialise_API_object(attr_value)
        return serialized_data
    elif isinstance(obj, list):
        return [serialise_API_object(item) for item in obj]
    else:
        return obj






