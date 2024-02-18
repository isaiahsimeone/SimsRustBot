import * as socketio from "./socketio.js";

const DEBUG = true;

export let server = null;

export function initialiseServer() {
    log("Server init");
    socketio.make_request("serverinfo");
}

export function receiveServerInfo(data) {
    data = data.data;
    log("Got server info: " + JSON.stringify(data));
    server = data;
}



function log(...args) {
	if (DEBUG)
        console.log("%c[server.js] ", "color: #28B463", ...args);
}