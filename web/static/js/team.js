//@ts-check
import * as socketio from "./socketio.js";
import { Member, TeamInfo } from "./structures.js";
//import { receiveMapNotes } from "./note.js";
import { receiveTeamMembers, nameFromSteamId, steamImageExists } from "./steam.js";
import * as util from "./util.js";
import { snapToPlayer } from "./map.js";
//import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;

/**
 * @type {TeamInfo}
 */
export let teamInfoInstance;

/**
 * @type {Set}
 * Contains steam IDs of players whose map notes
 * should be hidden
 */
let hidden_player_notes = new Set();

/**
 * Initialises the variable 'team_info' by requesting 
 * the data from the flask server
 */
export async function initialiseTeam() {
    const teamData = await socketio.request_topic("team_info");
    teamInfoInstance = new TeamInfo(teamData.team_info);
    // Initialise steam id's and names
    receiveTeamMembers(teamInfoInstance.members);
    createTeamInfoPanel();
}

export async function teamMemberDied() {

}

export async function teamMemberSpawned() {

}

export async function teamMemberOffline() {

}

export async function teamMemberOnline() {

}

//export async function receiveTeam() {
//    initialiseTeam();
//}

//export async function removeTeamMember(removedMemberData) {



//export async function addTeamMember(newMemberData) {



//export async function updateTeamMember() {
    



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

function createTeamInfoPanel() {
    var target = util.safeGetId("team-info", log);
    target.innerHTML = "";
    var members = teamInfoInstance.members;
    for (let i = 0; i < members.length; i++) {
        target.appendChild(createPanelTeamMember(members[i]));
        setTeamMemberVital(members[i].steam_id, members[i].is_alive);
        setTeamMemberConnectivity(members[i].steam_id, members[i].is_online);
    }
}

export function isLeader(steam_id) {
    return steam_id == teamInfoInstance.leader_steam_id;
}

/**
 * 
 * @param {Member} member 
 */
function createPanelTeamMember(member) {
    var team_info_player = util.createDiv("team-info-player");
    team_info_player.id = `team-info-${member.steam_id}`;

    var team_info_col1 = util.createDiv("team-info-col");
    var team_info_player_image = util.createDiv("team-info-player-image");
    var steam_image_url;
    if (steamImageExists(member.steam_id))
        steam_image_url = `url("static/images/steam_pics/${member.steam_id}.png`;
    else {
        steam_image_url = `url("static/images/steam_pics/default.png")`;
        team_info_player_image.classList.add(`awaiting-image-${member.steam_id}`);
    }
    team_info_player_image.style.backgroundImage = steam_image_url;

    team_info_col1.appendChild(team_info_player_image);
    team_info_player.appendChild(team_info_col1);
   
    var team_info_col2 = util.createDiv("team-info-col");
    var team_info_player_name = util.createDiv("team-info-player-name");
    team_info_player_name.innerHTML = member.name;
    team_info_col2.appendChild(team_info_player_name);
    log (member.steam_id, teamInfoInstance.leader_steam_id);
    if (isLeader(member.steam_id)) {
        var team_info_player_crown = util.createDiv("team-info-player-crown");
        team_info_col2.appendChild(team_info_player_crown);
    }
    
    team_info_player.appendChild(team_info_col2);

    var team_info_col3 = util.createDiv("team-info-col");
    var team_info_player_button_group = util.createDiv("team-info-player-button-group");

    var team_info_button_accuracy = util.createDiv("team-info-player-button team-info-button-accuracy");
    team_info_button_accuracy.addEventListener("click", function(event) {
        snapToPlayer(member.steam_id);
    });

    var team_info_button_wrench = util.createDiv("team-info-player-button team-info-button-wrench");
    team_info_button_wrench.addEventListener("click", function(event) {
        createConfigDialog(event, member.steam_id);
    });

    if (member.is_online)
        team_info_player_button_group.appendChild(team_info_button_accuracy);

    var hide_map_notes_button = util.createDiv("team-info-player-button");

    if (hidden_player_notes.has(member.steam_id))
        hide_map_notes_button.classList.add("team-info-button-map-notes-hidden");
    else
        hide_map_notes_button.classList.add("team-info-button-map-notes-shown");
    
    //hide_map_notes_button.addEventListener("click", function(event) {
    //    toggleMapNoteVisibility(member.steam_id);
    //});
    
    team_info_player_button_group.appendChild(hide_map_notes_button);

    team_info_player_button_group.appendChild(team_info_button_wrench);
    
    team_info_col3.appendChild(team_info_player_button_group);
    
    team_info_player.appendChild(team_info_col3);
    
    return team_info_player;
}

function setTeamMemberVital(steam_id, is_alive) {
    var team_info_player_entry = document.getElementById(`team-info-${steam_id}`);
    if (!team_info_player_entry)
        return ;

    var player_image_list = team_info_player_entry.getElementsByClassName("team-info-player-image");
    if (!player_image_list || !player_image_list[0])
        return ;
    
    var player_image = player_image_list[0];
    var strike;
    if (is_alive) {
        // They're alive, remove strikethrough
        player_image.classList.remove("team-info-player-image-darken");
        strike = player_image.getElementsByClassName("team-info-player-image-strikethrough");
        if (!strike || !strike[0])
            return;
        strike[0].remove();
    } else {
        player_image.classList.add("team-info-player-image-darken");
        strike = util.createDiv("team-info-player-image-strikethrough");
        player_image.appendChild(strike);
    }
}

function setTeamMemberConnectivity(steam_id, is_online) {
    
}


export function teamMemberConnectivityChange(connectivityChange) {
    log("CONNECT/DISCONNECT");
}

export function teamMemberVitalChange(vitalChange) {
    log("DEATH/SPAWN");
    log(vitalChange);
    setTeamMemberVital(vitalChange.steam_id, vitalChange.is_alive);
}

function createConfigDialog(event, steam_id) {
    log("CLICK");
    const popup = util.safeGetId("player-config-popup", log);
    
    if (popup.classList.contains('config-popup-open')) {
        // Close the popup
        popup.classList.remove('config-popup-open');
      } else {
        // Open the popup
        popup.classList.add('config-popup-open');
      }
}


/**
 * Determines whether the operator of the bot (the bot owner) is in a rust team
 * @returns True if the bot owner is in a team
 */
//function bot_owner_in_team() {
//    return teamInfoInstance.leader_steam_id != 0;
//}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[team.js] ", "color: #FFA500", ...args);
}
