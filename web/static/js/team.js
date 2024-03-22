//@ts-check
import * as socketio from "./socketio.js";
//import { receiveMapNotes } from "./note.js";
//import { receiveTeamMembers } from "./steam.js";
//import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;

/**
 * @type {TeamInfo}
 */
export let teamInfoInstance;

export class TeamInfo {
    /**
     * @param {any} teamData
     */
    constructor(teamData) {
        this._data = teamData;
    }

    get leader_map_notes() { return this._data.map_notes.map((/** @type {any} */ note) => new MapNote(note)); }

    get leader_steam_id() { return this._data.leader_steam_id; }

    get map_notes() { return this._data.map_notes.map((/** @type {any} */ note) => new MapNote(note)); }

    get members() { return this._data.members.map((/** @type {any} */ member) => new Member(member)); }
}

export class MapNote {
    /**
     * @param {any} mapNoteData
     */
    constructor(mapNoteData) {
        this._data = mapNoteData;
    }

    get colour_index() { return this._data.colour_index; }

    get label() { return this._data.label; }

    get icon() { return this._data.icon; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
}

export class Member {
    /**
     * @param {any} memberData
     */
    constructor(memberData) {
        this._data = memberData;
    }

    get death_time() { return this._data.death_time; }

    get is_alive() { return this._data.is_alive; }

    get is_online() { return this._data.is_online; }

    get name() { return this._data.name; }

    get spawn_time() { return this._data.spawn_time; }

    get steam_id() { return this._data.steam_id; }

    get x() { return this._data.x; }

    get y() { return this._data.y; }
}

/**
 * Initialises the variable 'team_info' by requesting 
 * the data from the flask server
 */
export async function initialiseTeam() {
    const teamData = await socketio.request_topic("team_info");
    teamInfoInstance = new TeamInfo(teamData["team_info"]);
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
