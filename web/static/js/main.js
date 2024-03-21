//import { initialiseChat } from "./chat.js";
//import { initialiseMap } from "./map.js";
//import { initialiseTeam } from "./team.js";
//import { initialiseCommands } from "./command.js";
import { initialiseServer, server } from "./server.js";
//import { initialiseDialogs } from "./dialogs.js";
//import { awaitVariableSet } from "./util.js";

const DEBUG = true;

export let img_path = "static/images";

$(document).ready(function () {
	init();
});

async function init() {
	console.log('%cSimsRustBot', 'font-size: 40px; color: #c33e29; text-shadow: 3px 3px #000; font-weight: bold;');
	
	initialiseServer();

    /*Wait for server to be defined */
	await awaitVariableSet(() => server !== null); // Wait for 'server' to be defined
	
	//initialiseTeam();

	//initialiseMap();

	//initialiseChat();

	//initialiseCommands();

	//initialiseDialogs();
}


function log(...args) {
	if (DEBUG)
		console.log("%c[main.js] ", "color: #C70039", ...args);
}