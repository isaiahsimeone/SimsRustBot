import * as socketio from "./socketio.js";
import { receiveMapNotes } from "./note.js";
import { receiveTeamMembers } from "./steam.js";
import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;

export let team_info = null;
export let player_is_in_team = false;

export function initialiseTeam() {
    log("Server init");
    socketio.make_request("teaminfo");
}

export function receiveTeamInfo(data) {
    data = data.data;
    log("Got team info: " + JSON.stringify(data));    
    team_info = data;

    // Not in a team if leader steam ID is 0
    player_is_in_team = team_info.leader_steam_id != 0;
    toggleChatAvailability(player_is_in_team);

    // Get steam names from steam IDs
    receiveTeamMembers(team_info['members'])

    // Call map.js to plot map notes
    receiveMapNotes(team_info['map_notes'])
}



function log(...args) {
	if (DEBUG)
        console.log("%c[team.js] ", "color: #FFA500", ...args);
}