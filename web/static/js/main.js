import { initialiseChat } from "./chat.js";
import { initialiseMap } from "./map.js";
import { initialiseServer, server } from "./server.js";
import { awaitVariableSet } from "./util.js";

const DEBUG = true;

// Global variables

export let img_path = "static/images";


let map_monument_data = null;
let server_info_data = null

// RustInfo[url=, name=Sims Server, map=Procedural Map, size=4000, players=0, max_players=5, queued_players=0, seed=793197, wipe_time=1707127438, header_image=, logo_image=]

// TODO: when heli/cargo is coming in, specify the direction that the player can align their compass to. Just a vector

let MAP_SZ = null;

$(document).ready(function () {
	init();
});

async function init() {
	// Initialise the buttons

	// Initialise the server - and await server to become defined
	initialiseServer();
	await awaitVariableSet(() => server !== null);

	// Initialise the map
	initialiseMap();

	// Initialise the chat
	initialiseChat();
}


function getServerInfo(data) {
	log("SERVER INFO keys: " + Object.keys(data));
	server_info_data = data;
	// Get map size
	let map_size = data.size
	MAP_SZ = map_size;
	log("Map size is " + MAP_SZ);
}




// Also sets the background colour
function getMapMonuments(data) {
	// Also sets background colour
	mapContainer.style.backgroundColor = data.background;

	// Receive monument data
	map_monument_data = data.monuments;

	redrawMonuments();
}

function redrawMonuments() {
	// delete current monument text
	deleteAllMapText();

	for (let i = 0; i < Object.keys(map_monument_data).length; i++) {
		let text = MonumentNames[map_monument_data[i].token];
		if (text)
			createMapText(i, map_monument_data[i].x, map_monument_data[i].y, text);
	}
}





function updateInitialMapRect() {
	if (mapImage) {
		initialMapRect = mapImage.getBoundingClientRect();
	}
}


function setOverlay(overlayId, jsonX, jsonY, rotation) {

	const overlay = document.getElementById(overlayId);

	if (!overlay || !initialMapRect)
		return;

	// Overlay dimensions
	const overlay_width = overlay.offsetWidth;
	const overlay_height = overlay.offsetHeight;
	const overlay_width_center = overlay_width / 2;
	const overlay_height_center = overlay_height / 2;


	// position calculations
	const scaleX = initialMapRect.height / MAP_SZ; // I have no idea why we use the image height here, but it works
	const scaleY = initialMapRect.height / MAP_SZ;
	const jsonY_flipped = MAP_SZ - jsonY // Flip the Y-coordinate

	// Convert map coordinates (jsonX, jsonY) to image pixel coordinates
	const imageX = scaleX * jsonX + map_image_offset_left - overlay_width_center;
	const imageY = scaleY * jsonY_flipped + initialMapRect.top - overlay_height_center;

	const invertedScale = 1 / panzoom.getScale();

	// Apply the background image and position the overlay
	overlay.style.transform = `translate(${imageX}px, ${imageY}px) scale(${invertedScale}) rotate(${rotation}deg)`;
	overlay.style.display = 'block'; // Show the overlay

	// Store the initial positions
	overlay.dataset.initialX = imageX;
	overlay.dataset.initialY = imageY;
	overlay.dataset.initialRotation = rotation;

}

// places an overlay image on the map given JSON coordinates
// from the RustAPI. It will be converted to coordinates suitable
// for the map image displayed in browser
function setOverlayImage(overlayId, image, is_player = false) {
	const overlay = document.getElementById(overlayId);

	if (!overlay)
		return;
	if (!is_player)
		overlay.style.backgroundImage = `url('${img_path}/rust/${image}')`;
	else
		overlay.style.backgroundImage = `url('${img_path}/steam_pics/${image}.png')`;


}

// Adjust overlays on zoom
function adjustOverlaysOnZoom() {
	const overlays = document.getElementsByClassName("overlay");

	for (let i = 0; i < overlays.length; i++) {
		adjustOverlayPositionZoom(overlays[i].id);
	}
}

// Adjust individual overlay position
function adjustOverlayPositionZoom(overlayId) {
	const overlay = document.getElementById(overlayId);

	if (overlay) {
		// Overlay size changes depending on panzoom scale
		const invertedScale = 1 / panzoom.getScale();

		// Retrieve initial positions from dataset
		const initialX = parseFloat(overlay.dataset.initialX);
		const initialY = parseFloat(overlay.dataset.initialY);

		// Calculate the center position of the overlay
		const centerX = initialX + overlay.offsetWidth / 2 * invertedScale;
		const centerY = initialY + overlay.offsetHeight / 2 * invertedScale;

		// Adjust the position to account for the scaling
		const adjustedX = centerX - (overlay.offsetWidth / 2 * invertedScale);
		const adjustedY = centerY - (overlay.offsetHeight / 2 * invertedScale);

		const rotation = overlay.dataset.initialRotation;

		// Apply the new transform
		overlay.style.transform = `translate(${adjustedX}px, ${adjustedY}px) scale(${invertedScale}) rotate(${rotation}deg)`;

	}
}

function deleteAllMapMarkers() {
	var elements = document.getElementsByClassName("overlay");

	Array.from(elements).forEach((element) => {
		if (!element.classList.contains("map_text")) // Don't delete text
			element.remove(); // Removes the element from the DOM
	});
}

function deleteAllMapText() {
	var elements = document.getElementsByClassName("map_text");

	Array.from(elements).forEach((element) => {
		element.remove(); // Removes the element from the DOM
	});
}

// Update map markers
function updateMapMarkers() {
	if (!map_marker_data)
		return;

	for (let i = 0; i < map_marker_data.length; i++) {

		let overlay_img = null;
		let marker = map_marker_data[i];
		let marker_type = marker.type;
		let rotation = 360 - map_marker_data[i].rotation;

		let x = map_marker_data[i].x;
		let y = map_marker_data[i].y;

		let is_player = false;

		const overlay = document.createElement("div");
		overlay.className = "overlay";
		overlay.id = "overlay" + i;

		overlay_img = marker_type_to_img[marker_type]; // May change in switch

		switch (marker_type) {
			case markers.PLAYER:
				is_player = true;
				overlay.style.zIndex = 4; // Always on top				
				overlay.style.width = scaledDim(21);
				overlay.style.height = scaledDim(21);
				overlay.classList.add("circle-image");
				overlay_img = steamPictureOrDefault(marker.steam_id);
				log(map_marker_data[i]);
				log("ABA " + marker.steam_id);
				createMapText(overlay.id + "steamname", x, y - 20, nameFromSteamId(marker.steam_id).toUpperCase());
				break;
			case markers.SHOP:
				overlay_img = marker.out_of_stock ? marker_type_to_img[markers.SHOP][1] : marker_type_to_img[markers.SHOP][0];
				overlay.style.width = scaledDim(12);
				overlay.style.height = scaledDim(12);
				break;
			case markers.CHINOOK:
				overlay_img = marker_type_to_img[markers.CHINOOK][0];
				overlay.style.width = scaledDim(40);
				overlay.style.height = scaledDim(40);

				var theta = rotation * Math.PI / 180;
				var magnitude = parseInt(overlay.style.width.replace("px", "")) * (1 / panzoom.getScale()) * 1.3;
				var blade_x = magnitude * Math.sin(theta);
				var blade_y = magnitude * Math.cos(theta);

				// Draw blades
				drawBlades("overlay" + i + "blades", marker_type_to_img[markers.CHINOOK][1], x + blade_x, y + blade_y);
				drawBlades("overlay" + i + "blades2", marker_type_to_img[markers.CHINOOK][1], x - blade_x, y - blade_y);
				break;
			case markers.CARGO:
				overlay.style.width = scaledDim(35);
				overlay.style.height = scaledDim(35);

				break;
			case markers.HELI:
				overlay_img = marker_type_to_img[markers.HELI][0];
				overlay.style.width = scaledDim(40);
				overlay.style.height = scaledDim(40);

				// Draw blades

				var theta = rotation * Math.PI / 180;
				var magnitude = parseInt(overlay.style.width.replace("px", "")) * (1 / panzoom.getScale()) * 0.7;
				var blade_x = magnitude * Math.sin(theta);
				var blade_y = magnitude * Math.cos(theta);



				drawBlades("overlay" + i + "blades", marker_type_to_img[markers.HELI][1], x + blade_x, y + blade_y);


				break;
		}

		document.getElementById("map-container").appendChild(overlay);
		setOverlayImage(overlay.id, overlay_img, is_player);
		setOverlay(overlay.id, x, y, rotation);
	}

}

function drawBlades(overlayId, img, x, y) {

	const blades = document.createElement("div");
	blades.className = "overlay blades";
	blades.id = overlayId;
	blades.style.width = scaledDim(30);
	blades.style.height = scaledDim(30);
	blades.style.zIndex = 1;

	document.getElementById("map-container").appendChild(blades);

	applyRotation(overlayId);
	setOverlayImage(overlayId, img);
	setOverlay(overlayId, x, y, 0);
}



function scaledDim(num) {
	return String(num * (MAP_SZ / 3000)) + "px"
}



function log(...args) {
	if (DEBUG)
		console.log("[main.js] ", ...args);
}