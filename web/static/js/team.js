//@ts-check
import * as socketio from "./socketio.js";
import { TeamInfo } from "./structures.js";
//import { receiveMapNotes } from "./note.js";
//import { receiveTeamMembers } from "./steam.js";
//import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;

/**
 * @type {TeamInfo}
 */
export let teamInfoInstance;


/**
 * Initialises the variable 'team_info' by requesting 
 * the data from the flask server
 */
export async function initialiseTeam() {
    const teamData = await socketio.request_topic("team_info");
    teamInfoInstance = new TeamInfo(teamData.team_info);
}

/**
 * Determines whether the operator of the bot (the bot owner) is in a rust team
 * @returns True if the bot owner is in a team
 */
function bot_owner_in_team() {
    return teamInfoInstance.leader_steam_id != 0;
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[team.js] ", "color: #FFA500", ...args);
}
