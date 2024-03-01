
import { my_steam_id, nameFromSteamId, steamPictureOrDefault } from "./steam.js";
import { img_path } from "./main.js";
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

export function toggleChatAvailability(is_available) {
	log("chat is:", is_available);
	let chatMessageBox = document.getElementById("chatMessage");
	let joinATeam = document.getElementById("chat-join-a-team-first");
	let messageContainer = document.getElementById("messages_container");

	chatMessageBox.disabled = !is_available;

	if (!is_available) {
		joinATeam.style.display = "flex";
		messageContainer.style.visibility = "hidden";
	} else {
		joinATeam.style.display = "none";
		messageContainer.style.visibility = "visible";
	}
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

	// Remove bot and player tag from beginning
	const pattern = /^\[BOT\] \[[^\]]+\]/;
	message_txt = message_txt.replace(pattern, '').trim();


	let messages_container = document.getElementById("messages_container");

	if (!messages_container)
		return ;
	
	// Create message header
	const header = document.createElement("div");
	header.className = "chat-message-header";

	// Header image
	const headerImage = document.createElement("div");
	headerImage.className = "chat-message-header-image circle-image player";
	headerImage.style.height = "25px";
	headerImage.style.width = "25px";
	headerImage.style.backgroundImage = `url('${img_path}/steam_pics/${sender_steam_id}.png')`; // it'll be available eventually
	
	const headerName = document.createElement("div");
	headerName.className = "chat-message-header-name";
	headerName.innerHTML = nameFromSteamId(sender_steam_id);
	
	header.appendChild(headerImage);
	header.appendChild(headerName);
	// overlay.style.backgroundImage = `url('${img_path}/steam_pics/${image}.png')`;

	// Create message body
	const message = document.createElement("div");
	message.className = "chat-message";
	message.innerHTML = message_txt;

	if (sender_steam_id == my_steam_id)
		message.classList.add("me");
	else
		message.classList.add("other");

	// insert message header, then body
	message.insertBefore(header, message.firstChild);
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