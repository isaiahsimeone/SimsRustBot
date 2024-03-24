//@ts-check
import * as socketio from "./socketio.js";
import { ServerInfo } from "./structures.js";

const DEBUG = true;

/**
 * @type {ServerInfo}
 */
export let serverInfoInstance;

/**
 * Initialises the variable 'serverInfoInstance' by requesting
 * the data from the flask server and wrapping it in a ServerInfo instance
 */
export async function initialiseServer() {
    const serverData = await socketio.request_topic("server_info");
    serverInfoInstance = new ServerInfo(serverData["server_info"]);
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[server.js] ", "color: #28B463", ...args);
}