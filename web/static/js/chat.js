
import { my_steam_id } from "./script.js";

let team_chat_stream = null;
$(document).ready(function() {



        team_chat_stream = new EventSource('/teamchat');
        team_chat_stream.addEventListener('message', getTeamMessagesFromES, false);
});

function processTeamChatData(data) {
    console.log(data);
    let messages = data;
	for (let i = 0; i < messages.length; i++) {
		if (messages[i]) {
            console.log("ADDMSG(" + messages[i].steam_id + " " + messages[i].message + ")")
            addMessageToChat(messages[i].steam_id, messages[i].message);
        }
	}
}

function addMessageToChat(sender_steam_id, message_txt) {
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

		//<div class="chat-message other">This is a chat message from someone else</div>
		//<div class="chat-message me">This is a chat message from me</div>


}




function getTeamMessagesFromES(data) {
	processTeamChatData(JSON.parse(data.data));
}