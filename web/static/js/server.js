import * as socketio from "./socketio.js";

const DEBUG = true;

export let server = null;

export function initialiseServer() {
    log("Server init");
    let sinfo = socketio.request_topic("server_info");
    log(sinfo);
}

export function receiveServerInfo(data) {
    log("Got server info: " + JSON.stringify(data));
    server = data;
}



function log(...args) {
	if (DEBUG)
        console.log("%c[server.js] ", "color: #28B463", ...args);
}