import { Member } from "./structures.js";
import { getCookie } from "./util.js";

const DEBUG = true;

let steamIdToNameMap = {};
let steam_images_available = [];

export let my_steam_id = getCookie("steam_id");

/**
 * Receive a list of rust team members. Then,
 * create a map of their steam name to steam id
 * and download their steam image
 * @param {Member[]} members 
 */
export function receiveTeamMembers(members) {
    for (let i = 0; i < members.length; i++) {
        if (!steamImageExists(members[i].steam_id)) {
            steamIdToNameMap[members[i].steam_id] = members[i].name;
            downloadSteamImage(members[i].steam_id);
        }
    }
    log("Your steam name is", nameFromSteamId(my_steam_id));
}

export function nameFromSteamId(steamId) {
    return steamIdToNameMap[steamId] || "Unknown";
}

export function steamImageExists(steam_id) {
    return steam_images_available.includes(steam_id);
}


export function downloadSteamImage(steamId) {
    log("Downloading steam profile pic for", steamId);
    const url = `${window.location.href}downloadsteamimage/${steamId}`;

    fetch(url, {
        method: 'POST',
    })
        .then(response => response.json()) // Assuming JSON response
        .then(data => {
            if (data.success) {
                // Image processing started, now poll for availability or proceed as necessary
                log(data.message);
                steam_images_available.push(steamId);
                // Elements might be marked waiting for this image. Update the image of that element
                updateWaitingElements(steamId);
                // Optionally, implement polling mechanism here if you need to wait for the image to be available
            } else {
                // Handle failure
                console.error("Failed to download image for", steamId, ":", data.message);
                // Create default image for their ID.
            }
        })
    .catch(error => console.error('Error during fetch operation:', error));
}

function updateWaitingElements(steam_id) {
    var wait_tag = `awaiting-image-${steam_id}`;
    var waiters = document.getElementsByClassName(wait_tag);
    for (let i = 0; i < waiters.length; i++) {
        waiters[i].style.backgroundImage = `url("static/images/steam_pics/${steam_id}.png`;
        waiters[i].classList.remove(wait_tag);
    }
}

function log(...args) {
	if (DEBUG)
        console.log("%c[steam.js] ", "color: #3498DB", ...args);
}