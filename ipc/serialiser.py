import json
from enum import Enum, auto
from rustplus import RustTeamMember, RustTeamNote, RustTeamInfo

class_mappings = {
    RustTeamMember: ['steam_id', 'name', 'x', 'y', 'is_online', 'spawn_time', 'is_alive', 'death_time'],
    RustTeamNote: ['type', 'x', 'y', 'icon', 'colour_index', 'label'],
    RustTeamInfo: ['leader_steam_id', 'members', 'map_notes', 'leader_map_notes']
}


def serialise_API_object(obj):
    obj_type = type(obj)
    if obj_type in class_mappings:
        serialized_data = {}
        for attr in class_mappings[obj_type]:
            attr_value = getattr(obj, attr)
            if type(attr_value) in class_mappings:
                serialized_data[attr] = serialise_API_object(attr_value)
            else:
                serialized_data[attr] = attr_value
        return serialized_data
    else:
        return obj
