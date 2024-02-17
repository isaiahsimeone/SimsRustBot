
import { my_steam_id } from "./steam.js";
import * as socketio from "./socketio.js";

const DEBUG = false;

export function initialiseChat() {
	// Request the chat
	socketio.make_request("teamchat");
}

export function receiveTeamChatData(data) {
	log('Received team chat update:', data);
	processTeamChatData(data);
}

function processTeamChatData(data) {
    let messages = data;

	for (let i = 0; i < messages.length; i++)
		if (messages[i])
            addMessageToChat(messages[i].steam_id, messages[i].message);
}

function addMessageToChat(sender_steam_id, message_txt) {
	log("Adding Message: (" + sender_steam_id + " " + message_txt + ")")

	let messages_container = document.getElementById("messages_container");

	if (!messages_container)
		return ;
	
	// TODO: add player name to message

	const message = document.createElement("div");
	message.className = "chat-message";
	message.innerHTML = message_txt;

	if (sender_steam_id == my_steam_id)
		message.classList.add("me");
	else
		message.classList.add("other");

	messages_container.appendChild(message);
}


function log(...args) {
	if (DEBUG)
		console.log("[chat.js] ", ...args);
}