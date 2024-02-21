import * as socketio from "./socketio.js";
import { receiveMapNotes } from "./note.js";
import { receiveTeamMembers } from "./steam.js";

const DEBUG = true;

export let team_info = null;

export function initialiseTeam() {
    log("Server init");
    socketio.make_request("teaminfo");
}

export function receiveTeamInfo(data) {
    data = data.data;
    log("Got team info: " + JSON.stringify(data));
    team_info = data;

    // Get steam names from steam IDs
    receiveTeamMembers(team_info['members'])

    // Call map.js to plot map notes
    receiveMapNotes(team_info['map_notes'])
}



function log(...args) {
	if (DEBUG)
        console.log("%c[team.js] ", "color: #FFA500", ...args);
}