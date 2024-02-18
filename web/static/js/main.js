import { initialiseChat } from "./chat.js";
import { initialiseMap } from "./map.js";
import { initialiseTeam } from "./team.js";
import { initialiseCommands } from "./command.js";
import { initialiseServer, server } from "./server.js";
import { awaitVariableSet } from "./util.js";

const DEBUG = true;

export let img_path = "static/images";

// TODO: when heli/cargo is coming in, specify the direction that the player can align their compass to. Just a vector


$(document).ready(function () {
	init();
});

async function init() {
	console.log('%cSimsRustBot', 'font-size: 40px; color: #c33e29; text-shadow: 3px 3px #000; font-weight: bold;');
	
	initialiseServer();
	await awaitVariableSet(() => server !== null); // Wait for response to define 'server'
	
	initialiseTeam();
	// Wait here for team set

	initialiseMap();

	initialiseChat();

	initialiseCommands();
}


function log(...args) {
	if (DEBUG)
		console.log("%c[main.js] ", "color: #C70039", ...args);
}