//import { initialiseChat } from "./chat.js";
import { initialiseMap } from "./map.js";
//import { initialiseCommands } from "./command.js";
import { initialiseTeam, teamInfoInstance } from "./team.js";
import { initialiseServer } from "./server.js";
import { initialiseMapNotes } from "./map_notes.js";
//import { initialiseDialogs } from "./dialogs.js";
import * as chat from "./chat.js";

const DEBUG = true;

export let img_path = "static/images";

$(document).ready(function () {
	init();
});

async function init() {
	console.log('%cSimsRustBot', 'font-size: 40px; color: #c33e29; text-shadow: 3px 3px #000; font-weight: bold;');
	
	await initialiseServer();

	await initialiseTeam();

	await initialiseMap();

	initialiseMapNotes();

	await chat.initialiseChat();

	//initialiseCommands();

	//initialiseDialogs();
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
		console.log("%c[main.js] ", "color: #C70039", ...args);
}