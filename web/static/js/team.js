//@ts-check
import * as socketio from "./socketio.js";
import { TeamInfo } from "./structures.js";
//import { receiveMapNotes } from "./note.js";
import { receiveTeamMembers, nameFromSteamId } from "./steam.js";
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
    // Initialise steam id's and names
    receiveTeamMembers(teamInfoInstance.members);    
}

export async function receiveTeam() {
    receiveTeamMembers(teamInfoInstance.members);
}

export async function removeTeamMember(removedMemberData) {

}

export async function addTeamMember(newMemberData) {

}

export async function updateTeamMember() {
    
}


export function getSpawnTime(steam_id) {
    var target = teamInfoInstance.getMemberBySteamId(steam_id);
    if (!target || !target.spawn_time)
        return -1;
    return target.spawn_time;
}

export function getDeathTime(steam_id) {
    var target = teamInfoInstance.getMemberBySteamId(steam_id);
    if (!target || !target.death_time)
        return -1;
    return target.death_time;
}

export function getName(steam_id) {
    return nameFromSteamId(steam_id);
}

export function leaderSteamId(steam_id) {
    return teamInfoInstance.leader_steam_id;
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
