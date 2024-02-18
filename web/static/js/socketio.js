import { receiveTeamChatData } from "./chat.js";
import { receiveMapMarkerData, receiveMapMonuments } from "./map.js";
import { receiveTeamInfo } from "./team.js";
import { receiveServerInfo } from "./server.js";

const DEBUG = true;

export var socket = io.connect('http://' + location.host);

socket.on('connect', function() {
    log('Connected to the server');
});

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
            log("Encountered unknown broadcast type");
    }
});


socket.on("data_response", function(response) {
    let type = response.type;
    let data = response.data;

    log("Got data from server with type=" + type);

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
            log("Encountered unknown request type");
    }
});

export function send_to_server(what, data) {
    socket.emit("client_send", {type: what, data: data});
}

export function make_request(what) {
	socket.emit("request", {type: what});
}

function log(...args) {
	if (DEBUG)
		console.log("%c[socketio.js] ", "color: #FF00FF", ...args);
}