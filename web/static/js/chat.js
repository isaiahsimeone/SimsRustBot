import * as socketio from "./socketio.js";
import * as structures from "./structures.js";
import * as util from "./util.js";
import { my_steam_id, nameFromSteamId } from "./steam.js";

const DEBUG = true;

/**
 * @type {structures.Chat[]}
 */
let initial_chat_messages = [];

export async function initialiseChat() {
    // Listen for a click on the send message button
	document.getElementById("sendMessageBtn").addEventListener("click", sendTeamMessage);

	// Listen for enter pressed on text box
	document.getElementById("chatMessageInput").addEventListener("keyup", ({key}) => {
		if (key === "Enter")
			sendTeamMessage();
	});

    // Get initial team chat
    log("requesting initial chat msgs");
    let initial_chat_messages_raw = (await socketio.request_topic("team_chat_full")).messages;

    for (let i = 0; i < initial_chat_messages_raw.length; i++)
        initial_chat_messages.push(new structures.Chat(initial_chat_messages_raw[i]));
    
    log("got them", initial_chat_messages)
    for (let i = 0; i < initial_chat_messages.length; i++) {
        addTeamChat(initial_chat_messages[i]);
    }

}

/**
 * Add a team chat to the chat panel
 * @param {structures.Chat} message The message to add to the team chat
 */
export function addTeamChat(message) {
    log("Got team chat:", message);

    let messages_container = document.getElementById("messages_container");

	if (!messages_container)
		return ;
	
	// Create message header
	const header = document.createElement("div");
	header.className = "chat-message-header";

	// Header image
	const headerImage = document.createElement("div");
	headerImage.className = `chat-message-header-image circle-image player awaiting-image-${message.steam_id}`;
	headerImage.style.height = "25px";
	headerImage.style.width = "25px";
	headerImage.style.backgroundImage = `url('static/images/steam_pics/${message.steam_id}.png')`;
	
	const headerName = document.createElement("div");
	headerName.className = "chat-message-header-name";
	headerName.innerHTML = message.name;
	
	header.appendChild(headerImage);
	header.appendChild(headerName);

	// Create message body
	const message_body = document.createElement("div");
	message_body.className = "chat-message";
	message_body.innerHTML = message.message;

	if (message.steam_id == my_steam_id)
        message_body.classList.add("me");
	else
        message_body.classList.add("other");

	// insert message header, then body
	message_body.insertBefore(header, message_body.firstChild);
	messages_container.appendChild(message_body);
	// adjust scroll bar of messages field
	const container = document.getElementById("messages_container")
	container.scrollTop = container.scrollHeight;
}

function sendTeamMessage() {
	let message = document.getElementById("chatMessageInput").value;
	if (!message)
		return ;
	document.getElementById("chatMessageInput").value = "";
	let data = {steam_id: my_steam_id, name: nameFromSteamId(my_steam_id),
                message: message, colour: "#af5", time: util.timeNow()};

	socketio.send_to_server("team_message", data);

	log("Sent teamchat (" + message + ") to server");
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
		console.log("%c[chat.js] ", "color: #8b008b", ...args);
}