
from rustplus.api.structures.serialization import Serializable

class ExtendedRustTeamNote(Serializable):
    def __init__(self, rust_team_note, steam_id):
        self._note = rust_team_note
        self._steam_id = str(steam_id)
        
    @property
    def note(self) -> str:
        return self._note

    @property
    def steam_id(self) -> str:
        return self._steam_id
