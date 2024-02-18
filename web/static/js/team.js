import * as socketio from "./socketio.js";

const DEBUG = true;

export let team = null;

export function initialiseTeam() {
    log("Server init");
    socketio.make_request("teaminfo");
}

export function receiveTeamInfo(data) {
    data = data.data;
    log("Got team info: " + JSON.stringify(data));
    team = data;
}



function log(...args) {
	if (DEBUG)
        console.log("%c[team.js] ", "color: #FFA500", ...args);
}