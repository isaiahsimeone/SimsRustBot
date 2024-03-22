//@ts-check
import * as socketio from "./socketio.js";

const DEBUG = true;

/**
 * @type {ServerInfo}
 */
export let serverInfoInstance;

export class ServerInfo {
    /**
     * @param {any} serverData
     */
    constructor(serverData) {
        this._data = serverData;
    }

    get header_image() { return this._data.header_image; }

    get logo_image() { return this._data.logo_image; }

    get map() { return this._data.map; }

    get max_players() { return this._data.max_players; }
    
    get name() { return this._data.name; }

    get player_count() { return this._data.players; }

    get queued_players() { return this._data.queued_players; }

    get map_seed() { return this._data.seed; }

    get map_size() { return this._data.size; }

    get url() { return this._data.url; }

    get wipe_time() { return this._data.wipe_time; }
}

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