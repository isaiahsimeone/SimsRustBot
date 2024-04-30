
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, List

import loguru

from ipc.data_models import TeamInfo, TeamJoined, TeamLeaderChange, TeamLeft, TeamMapNotes, TeamMemberConnectivity, TeamMemberJoin, TeamMemberLeft, TeamMemberVital
from rust_socket.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass

from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from rustplus import RustSocket
from rustplus.api.structures.rust_info import RustInfo
from rustplus.api.structures.rust_team_info import RustTeamInfo, RustTeamMember, RustTeamNote


class TeamPollerService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus) -> None:
        super().__init__(bus, self.__class__.__name__)
        self.bus = bus
        self.config = {}
        self.socket: RustSocketManager
        
        self.server_info: RustInfo
        
        self.poll_rate = 999
        self.last_team_info: RustTeamInfo = None # type: ignore
        
    @loguru.logger.catch
    async def execute(self: TeamPollerService) -> None:
        await self.subscribe("team_info_event")
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        # Block until socket ready
        await self.last_topic_message_or_wait("socket_ready")
        # Set the socket
        self.socket = await RustSocketManager.get_instance()
        # Set team polling frequency
        self.poll_rate = int(self.config["RustPlusAPIService"]["team_polling_frequency"])
        # Get server info - RustPlusAPIService publishes this on startup to save tokens
        self.server_info = (await self.last_topic_message_or_wait("server_info")).data["server_info"]

        message = f"Team polling will occur every {self.poll_rate} seconds"
        if self.poll_rate < 5:
            message += "- This is fast, you may be rate limited."
            self.warning(message)
        else:
            self.info(message)
        
        # Team polling loop
        while True:
            await self.poll_team()
            await asyncio.sleep(self.poll_rate)
            
    async def poll_team(self, event=None) -> None:
        if event:
            # We get an event before we can compare it with anything. This will fail, so just exit
            if not self.last_team_info:
                return None
            team_info = event
        else:
            team_info = await self.socket.get_team_info()
        # Publish it to the bus, another service will probably use it
        await self.publish("team_info", TeamInfo(team_info=team_info))
        
        if self.last_team_info is None:
            self.last_team_info = team_info
            return None
      
        # Currently not in a team
        if team_info.leader_steam_id == 0:
            # Was in a team before
            if self.last_team_info.leader_steam_id != 0:
                # Left a team
                self.debug("Team left")
                await self.publish("team_left", TeamLeft())

        # Publish map notes to bus
        if not event:
            self.debug(f"Publish {len(team_info.map_notes)} map notes")
            await self.publish("team_map_notes", TeamMapNotes(map_notes=team_info.map_notes)) # type: ignore 
            print("team notes:", team_info.map_notes)
            print("leader notes:", team_info.leader_map_notes)
            
        # Currently in a team
        if team_info.leader_steam_id != 0:
            if self.last_team_info.leader_steam_id == 0:
                # Now in a team
                self.debug("Team joined")
                await self.publish("team_joined", TeamJoined())
            elif self.last_team_info.leader_steam_id != team_info.leader_steam_id:
                self.debug("team leader changed")
                await self.publish("team_leader_changed", TeamLeaderChange(new_leader_steam_id=team_info.leader_steam_id))
                
        member_changes = compare_team_info(self.last_team_info, team_info)
        
        for change in member_changes:
            print("Team member change:", change)
            match change:
                case {"added": member}:
                    await self.publish("team_member_join", TeamMemberJoin(member=member))
                    self.debug(f"MEMBER ADDED: {member.name}")
                case {"removed": member}:
                    await self.publish("team_member_left", TeamMemberLeft(member=member))
                    self.debug(f"MEMBER REMOVED: {member.name}")
                case {"steam_id": steam_id, "changes": specific_changes}:
                    for change_key, change_detail in specific_changes.items():
                        match change_key:
                            case "steam_id_changed":
                                self.debug("A members steamID changed?")
                            case 'name_changed':
                                self.debug(f"  Name changed from '{change_detail['from']}' to '{change_detail['to']}'")
                            case 'is_online_changed':
                                await self.publish("team_member_connectivity", TeamMemberConnectivity(steam_id=str(steam_id), is_online=change_detail['to']))
                                self.debug(f"  Online status changed from '{change_detail['from']}' to '{change_detail['to']}'")
                            case 'is_alive_changed':
                                await self.publish("team_member_vital", TeamMemberVital(steam_id=str(steam_id), is_alive=change_detail['to']))
                                self.debug(f"  Alive status changed from '{change_detail['from']}' to '{change_detail['to']}'")
                            case _:
                                self.error(f"Unknown change_key: {change_key}")
                            # Add more cases here if there are other types of changes you're tracking
                case _:
                    self.error(f"Unknown change: {change}")
        
        self.last_team_info = team_info
        
    
    async def on_message(self: TeamPollerService, topic: str, message: Message) -> None:
        match topic:
            case "team_info_event":
                self.warning("got the message")
                await self.poll_team(event=message.data["team_info"])
            case _:
                self.error(f"Encountered a message topic {topic} that i don't have a case for")
        self.debug(f"Bus message ({topic}):", message)

@staticmethod
def compare_team_info(last_info: RustTeamInfo, current_info: RustTeamInfo):
    # Comparison of members
    def member_comparison(prev_member: RustTeamMember, current_member: RustTeamMember):
        member_changes = {}
        # We don't care if a RustTeamMember x,y,death_time or spawn_time changes
        for attr in ['steam_id', 'name', 'is_online', 'is_alive']:
            prev_attr = getattr(prev_member, attr)
            current_attr = getattr(current_member, attr)
            if prev_attr != current_attr:
                member_changes[attr + '_changed'] = {'from': prev_attr, 'to': current_attr}
        return member_changes

    # Check for changes in team members list
    changes: List[dict[str, Any]] = []
    # Convert lists to dictionaries for easier lookup by steam_id
    prev_members_dict = {m.steam_id: m for m in last_info.members}
    current_members_dict = {m.steam_id: m for m in current_info.members}

    # Check for changes in existing members
    for steam_id, prev_member in prev_members_dict.items():
        current_member = current_members_dict.get(steam_id)
        if current_member:
            specific_changes = member_comparison(prev_member, current_member)
            if specific_changes:
                changes.append({'steam_id': steam_id, 'changes': specific_changes})

    # Check for added or removed members
    added_members = set(current_members_dict.keys()) - set(prev_members_dict.keys())
    removed_members = set(prev_members_dict.keys()) - set(current_members_dict.keys())
    
    for steam_id in added_members:
        changes.append({'added': current_members_dict[steam_id]})
    for steam_id in removed_members:
        changes.append({'removed': prev_members_dict[steam_id]})

    return changes