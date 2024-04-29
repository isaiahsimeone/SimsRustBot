
from rustplus.api.structures.serialization import Serializable
from rustplus.api.structures.rust_team_info import RustTeamNote
class ExtendedRustTeamNote(Serializable):
    def __init__(self, rust_team_note, steam_id):
        self._note: RustTeamNote = rust_team_note
        self._steam_id: str = str(steam_id)
        
    @property
    def note(self) -> RustTeamNote:
        return self._note

    @property
    def steam_id(self) -> str:
        return self._steam_id
