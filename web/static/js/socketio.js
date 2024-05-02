//@ts-check
//import { receiveTeamChatData } from "./chat.js";
import { receiveMarkers, removeMarker, setCreationTime } from "./map.js";
import * as util from "./util.js";
import * as team from "./team.js"; //{ initialiseTeam, teamMemberConnectivityChange, teamMemberVitalChange } from "./team.js";
import * as note from "./map_notes.js";
import * as chat from "./chat.js";
import * as structures from "./structures.js";
import * as device_manager from "./device_manager.js";
//import { receiveTeamInfo } from "./team.js";
//import { receiveServerInfo } from "./server.js";
//import { receiveWebMapNoteChange, receiveWebMapNotes } from "./note.js";

const DEBUG = true;

// @ts-ignore
export var socket = io.connect("http://" + location.host);

socket.on("connect", function() {
    log('Connected to the server');
});

socket.on("broadcast", function(/** @type {{ type: any; data: any; }} */ raw_data) {
    if (!raw_data)
        return ;

    let type = raw_data.type;

    let data = "NoData";
    let json_data = JSON.parse(raw_data["data"]);
    if (json_data)
        data = json_data["data"];

    switch (type) {
        case "map_markers":
            receiveMarkers(data["markers"]);
            break;
        case "team_map_notes":
            log("GOT TEAM MAP NOTES");
            note.receiveTeamMapNotes(data["map_notes"]);
            break;
        case "team_joined": log("Joined a team");
        case "team_left": log("Left a team");
        case "team_member_join": log("Someone joined the team");
        case "team_member_left": log("Someone left the team");
            team.initialiseTeam();
            break;
        case "team_member_vital":
            // Data is {steam_id, is_alive}
            team.teamMemberVitalChange(data);
            log("A player died/spawned");
            break;
        case "team_member_connectivity":
            team.teamMemberConnectivityChange(data);
            log("Someone joined or left");
            break;
        case "team_leader_changed":
            log("new team leader");
            break;
        case "heli_spawned":
            log("heli spawned");
            setCreationTime(data["id"], util.timeNow());
            break;
        case "heli_despawned":
            log("heli despawned");
            removeMarker(data["id"]);
            break;
        case "heli_downed":
            log("heli downed", data["id"]);
            removeMarker(data["id"]);
            break;
        case "chinook_spawned":
            log("chinook spawned");
            setCreationTime(data["id"], util.timeNow());
            break;
        case "chinook_despawned":
            log("chinook despawned");
            removeMarker(data["id"]);
            break;
        case "chinook_downed":
            log("chinook downed", data["id"]);
            removeMarker(data["id"]);
            break;
        case "marker_expired":
            log("Marker expired", data["id"]);
            removeMarker(data["id"]);
            break;
        case "explosion":
            log("explosion");
            setCreationTime(data["id"], util.timeNow());
            break;
        case "crate_dropped":
            log("Crate");
            setCreationTime(data["id"], util.timeNow());
            break;
        case "cargo_spawned":
            log("cargo spawned");
            setCreationTime(data["id"], util.timeNow());
            break;
        case "cargo_despawned":
            log("cargo despawned");
            removeMarker(data["id"]);
            break;
        case "team_message":
            log("Got team message");
            chat.addTeamChat(new structures.Chat(data));
        case "smart_alarm_message":
            log("Got an fcm notification", data);
            break;
        case "paired_devices":
            log("Got a list of paired devices", data);
            device_manager.receivePairedDevices(data);
            break;
        case "smart_switch_states":
            //log("Got smart switch states", data);
            device_manager.receiveSmartSwitchStates(data);
            break;
        default:
            log("Encountered unknown broadcast type:", type);
    }
});

/**
 * @param {string} topic
 */
function make_topic_request(topic) {
    return new Promise((resolve, reject) => {
        const onResponse = (data) => {
            cleanup();
            resolve(data);
        };

        const onError = (error) => {
            cleanup();
            reject(error);
        };

        const onTimeout = () => {
            cleanup();
            reject(new Error("Request timeout"));
        };

        const cleanup = () => {
            socket.off("response", onResponse);
            socket.off("error", onError);
            clearTimeout(timeoutId);
        };

        // 5 second timeout for the request
        const timeoutId = setTimeout(onTimeout, 5000);

        // Emit the request
        socket.emit("request_topic", {topic: topic});

        // Setup listeners
        socket.once("topic_response", onResponse);
        socket.once("error", onError);
    });
}

/**
 * @param {string} topic
 */
export async function request_topic(topic) {
    try {
        const data = await make_topic_request(topic);
        return JSON.parse(data["data"])["data"];
    } catch (error) {
        log("Error trying to get data for topic", topic, ":", error);
    }
    
}

export async function send_to_server(topic, data) {
    socket.emit("client_send", { topic: topic, data: data });
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
		console.log("%c[socketio.js]", "color: #FF00FF", ...args);
}