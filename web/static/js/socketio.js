//@ts-check
//import { receiveTeamChatData } from "./chat.js";
import { receiveMarkers } from "./map.js";
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
    let data = JSON.parse(raw_data["data"])["data"];
    switch (type) {
        case "map_markers":
            log("ADD");
            receiveMarkers(data["markers"]);
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

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
		console.log("%c[socketio.js]", "color: #FF00FF", ...args);
}