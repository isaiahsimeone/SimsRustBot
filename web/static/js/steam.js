import { getCookie } from "./util.js";

const DEBUG = true;

let steam_id_to_name = [];
let steam_images_available = [];

export let my_steam_id = getCookie("steam_id");

export function nameFromSteamId(steamId) {
    for (let i = 0; i < steam_id_to_name.length; i++)
        if (steam_id_to_name[i].steam_id === steamId)
            return steam_id_to_name[i].name;
    return "Unknown";
}

export function steamPictureOrDefault(steam_id) {
    if (steamImageExists(steam_id))
        return steam_id;
    return "default";
}

export function steamImageExists(steam_id) {
    log(steam_images_available.includes(steam_id));
    return steam_images_available.includes(steam_id);
}

export function downloadSteamImage(steamId) {
    log("downloading " + String(steamId));
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
                // Optionally, implement polling mechanism here if you need to wait for the image to be available
            } else {
                // Handle failure
                console.error("Failed to download image for", steamId, ":", data.message);
                // Create default image for their ID.
            }
        })
        .catch(error => console.error('Error during fetch operation:', error));
}

function log(...args) {
	if (DEBUG)
        console.log("%c[steam.js] ", "color: #3498DB", ...args);
}