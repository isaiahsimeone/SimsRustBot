
import { my_steam_id, nameFromSteamId } from "./steam.js";
import * as socketio from "./socketio.js";

const DEBUG = true;

export function initialiseChat() {
	// Listen for a click on the send message button
	document.getElementById("sendMessage").addEventListener("click", sendTeamMessage);

	// Listen for enter pressed on text box
	document.getElementById("chatMessage").addEventListener("keyup", ({key}) => {
		if (key === "Enter")
			sendTeamMessage();
	});

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
	// adjust scroll bar of messages field
	const container = document.getElementById("messages_container")
	container.scrollTop = container.scrollHeight;
}

function sendTeamMessage() {
	let message = document.getElementById("chatMessage").value;
	if (!message)
		return ;
	document.getElementById("chatMessage").value = "";
	let data = {message: message, sender: nameFromSteamId(my_steam_id)}
	socketio.send_to_server("teamchat", data);
	
	log("Sent teamchat (" + message + ") to server");
}

function log(...args) {
	if (DEBUG)
		console.log("%c[chat.js] ", "color: #DAF7A6", ...args);
}