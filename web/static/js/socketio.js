import { receiveTeamChatData } from "./chat.js";
import { receiveMapMarkerData, receiveMapMonuments } from "./map.js";
import { receiveServerInfo } from "./server.js";

const DEBUG = true;

export var socket = io.connect('http://' + location.host);

socket.on('connect', function() {
    log('Connected to the server');
    // Optionally, request the latest data after connecting
    socket.emit('request_update');
});

//socket.on('map_marker_update', function(data) {
//    log('Received map marker update:', data);
//});

socket.on("broadcast", function(raw_data) {
    if (!raw_data)
        return ;

    let type = raw_data.type;
    let data = raw_data.data;

    log("-- GOT BROADCAST FOR " + type + " --");

    switch (type) {
        case "teamchat":
            return receiveTeamChatData([data]);
        case "markers":
            return receiveMapMarkerData(data);
        case "monuments":
            return receiveMapMonuments(data);
        case "serverinfo":
            return receiveServerInfo(data);
        case "teaminfo":
            return receiveTeamInfo(data);
        default:
            log("Unknown broadcast type");
    }
});


socket.on("data_response", function(response) {
    let type = response.type;
    let data = response.data;

    log("Got response type: " + type + " data: " + data);

    switch (type) {
        case "teamchat":
            return receiveTeamChatData(data);
        case "serverinfo":
            return receiveServerInfo(data);
        case "teaminfo":
            return receiveTeamInfo(data);
        case "markers":
            return receiveMapMarkerData(data);
        case "monuments":
            return receiveMapMonuments(data);
        default:
            log("Unknown response type");
    }
});

export function make_request(what) {
	socket.emit("request", {type: what});
}

function log(...args) {
	if (DEBUG)
		console.log("[socketio.js] ", ...args);
}