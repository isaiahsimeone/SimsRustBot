/*import { receiveTeamChatData } from "./chat.js";
import { receiveMapMarkerData, receiveMapMonuments } from "./map.js";
import { receiveTeamInfo } from "./team.js";
import { receiveServerInfo } from "./server.js";
import { receiveWebMapNoteChange, receiveWebMapNotes } from "./note.js";
*/
const DEBUG = true;

export var socket = io.connect("http://" + location.host);

socket.on("connect", function() {
    log('Connected to the server');
});

socket.on("broadcast", function(raw_data) {
    if (!raw_data)
        return ;

    let type = raw_data.type;
    let data = raw_data.data;

    log("-- GOT BROADCAST FOR " + type + " --");

    switch (type) {

        default:
            log("Encountered unknown broadcast type:", type);
    }
});

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
        socket.emit("request_topic", {topic: topic}, (ack) => {
            if (!ack.success) {
                cleanup();
                reject(new Error("Failed to send request"));
            }
        });

        // Setup listeners
        socket.once("response", onResponse);
        socket.once("error", onError);
    });
}

export async function request_topic(topic) {
    try {
        const data = await make_topic_request(topic);
        log("Received data:", data);
    } catch (error) {
        log("Error trying to get data for topic", topic, ":", error);
    }
}


function log(...args) {
	if (DEBUG)
		console.log("%c[socketio.js]", "color: #FF00FF", ...args);
}