import { server } from "./server.js";
import { img_path } from "./main.js";
import * as socketio from "./socketio.js";
import * as createMarker from "./marker.js";

const DEBUG = true;

const mapImage = document.getElementById("map-image");
const mapContainer = document.getElementById("map-container")

export let panzoom = null;
let map_image_offset_left = 0;
let initial_map_rect = null;

let map_markers = null;
let map_monuments = null;
let map_notes = null;

export let panzoom_inverted_scale = 1;

export const markers = {
	PLAYER: 1,
	EXPLOSION: 2,
	SHOP: 3,
	CHINOOK: 4,
	CARGO: 5,
	CRATE: 6,
	RADIUS: 7,
	HELI: 8
};

const MonumentNames = {
	"airfield_display_name": "AIRFIELD",
	"bandit_camp": "BANDIT CAMP",
	"dome_monument_name": "THE DOME",
	"excavator": "GIANT EXCAVATOR PIT",
	"fishing_village_display_name": "FISHING VILLAGE",
	"gas_station": "OXUM'S GAS STATION",
	"harbor_2_display_name": "HARBOR",
	"harbor_display_name": "HARBOR",
	"junkyard_display_name": "JUNKYARD",
	"large_fishing_village_display_name": "LARGE FISHING VILLAGE",
	"large_oil_rig": "LARGE OIL RIG",
	"launchsite": "LAUNCH SITE",
	"lighthouse_display_name": "LIGHTHOUSE",
	"military_tunnels_display_name": "MILITARY TUNNEL",
	"mining_outpost_display_name": "MINING OUTPOST",
	"mining_quarry_hqm_display_name": "HQM QUARRY",
	"mining_quarry_stone_display_name": "STONE QUARRY",
	"mining_quarry_sulfur_display_name": "SULFUR QUARRY",
	"oil_rig_small": "OIL RIG",
	"outpost": "OUTPOST",
	"power_plant_display_name": "POWER PLANT",
	"satellite_dish_display_name": "SATELLITE DISH",
	"sewer_display_name": "SEWER BRANCH",
	"stables_a": "RANCH",
	"stables_b": "LARGE BARN",
	"supermarket": "ABANDONED SUPERMARKET",
	"swamp_c": "ABANDONED CABINS",
	"train_tunnel_display_name": "",
	"train_yard_display_name": "TRAIN YARD",
	"underwater_lab": "UNDERWATER LAB",
	"water_treatment_plant_display_name": "WATER TREATMENT PLANT",
	"ferryterminal": "FERRY TERMINAL",
	"arctic_base_a": "ARCTIC RESEARCH BASE",
	"missile_silo_monument": "MISSILE SILO",
	"AbandonedMilitaryBase": "ABANDONED MILITARY BASE"
}


// Map note type 0 is death marker, type 1 is a player set marker
// These are always the markers of the player running the bot
export function receiveMapNotes(notes) {
	log("I got map notes: " + JSON.stringify(notes));
	map_notes = notes;

	//redrawMapNotes();
}

export function receiveMapMarkerData(markers) {
	map_markers = markers;
	deleteAllMapMarkers();
	updateMapMarkers();
}

export function receiveMapMonuments(data) {
	let monuments_data = data.data

	mapContainer.style.backgroundColor = monuments_data.background; // Also gives us the background
	map_monuments = monuments_data.monuments;
	redrawMonuments();
}

export function initialiseMap() {
	socketio.make_request("markers");
	socketio.make_request("monuments");

	updateInitialMapRect();

	const panzoomElement = document.getElementById('panzoom-element');
	if (panzoomElement) {
		panzoom = Panzoom(panzoomElement, {
			maxScale: 6,
			contain: 'outside',
			animate: true,
		});

		panzoomElement.parentElement.addEventListener(
			'wheel',
			panzoom.zoomWithWheel
		);

		$(window).on('resize', function () {
			log(window.devicePixelRatio);
			panzoom_inverted_scale = 1 / panzoom.getScale();
			map_image_offset_left = getMapImageWhitespace();
			updateInitialMapRect();
			updateMapMarkers();
			redrawMonuments();
			adjustOverlaysOnZoom();
		});

		// Listen to Zoom events
		panzoomElement.addEventListener('panzoomzoom', function () {
			panzoom_inverted_scale = 1 / panzoom.getScale();
			updateMapMarkers();
			adjustOverlaysOnZoom();
		});
	}
	map_image_offset_left = getMapImageWhitespace();
}

function redrawMapNotes() {
	deleteAllMapNotes();
	for (let i = 0; i < Object.keys(map_monuments).length; i++) {
		let text = MonumentNames[map_monuments[i].token];
		if (text)
			createMapNote(i, map_monuments[i].x, map_monuments[i].y, colour, label);
	}
}

function createMapNote(id, x, y, colour, label) {
	
}

function redrawMonuments() {
	deleteAllMapText();
	for (let i = 0; i < Object.keys(map_monuments).length; i++) {
		let text = MonumentNames[map_monuments[i].token];
		if (text)
			createMapText(i, map_monuments[i].x, map_monuments[i].y, text);
	}
}

function createMapText(id, x, y, text) {
	let text_overlay = document.createElement("div");
	text_overlay.className = "overlay map_text";
	text_overlay.id = "overlay_text" + id;

	text_overlay.style.fontSize = "10px";
	text_overlay.innerHTML = text;

	mapContainer.appendChild(text_overlay);

	positionMarker(text_overlay.id, x, y, 0);
}

function updateInitialMapRect() {
	if (mapImage) {
		initial_map_rect = mapImage.getBoundingClientRect();
	}
}

function toImageCoords(x, y) {
	if (!initial_map_rect)
		return;

	const scaleX = initial_map_rect.height / server.size; // I have no idea why we use the image height here, but it works
	const scaleY = initial_map_rect.height / server.size;
	const jsonY_flipped = server.size - y; // Flip the Y-coordinate

	let translated_x = scaleX * x + map_image_offset_left;
	let translated_y = scaleY * jsonY_flipped + initial_map_rect.top;

	return { 'x': translated_x, 'y': translated_y };
}

export function positionMarker(overlayId, jsonX, jsonY, rotation = 0) {

	const overlay = document.getElementById(overlayId);

	if (!overlay || !initial_map_rect)
		return;

	// Overlay center points
	const overlay_width_center = overlay.offsetWidth / 2;
	const overlay_height_center = overlay.offsetHeight / 2;

	let { x, y } = toImageCoords(jsonX, jsonY);

	x -= overlay_width_center;
	y -= overlay_height_center;

	// Apply the background image and position the overlay
	overlay.style.transform = `translate(${x}px, ${y}px) scale(${panzoom_inverted_scale}) rotate(${rotation}deg)`;
	overlay.style.display = 'block'; // Show the overlay

	// Store the initial positions
	overlay.dataset.initialX = x;
	overlay.dataset.initialY = y;
	overlay.dataset.initialRotation = rotation;

}

// places an overlay image on the map given JSON coordinates
// from the RustAPI. It will be converted to coordinates suitable
// for the map image displayed in browser
export function setMarkerImage(overlayId, image) {
	const overlay = document.getElementById(overlayId);

	if (!overlay)
		return;

	if (overlay.dataset.is_player)
		overlay.style.backgroundImage = `url('${img_path}/steam_pics/${image}.png')`;
	else
		overlay.style.backgroundImage = `url('${img_path}/rust/${image}')`;
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
		// Retrieve initial positions from dataset
		const initialX = parseFloat(overlay.dataset.initialX);
		const initialY = parseFloat(overlay.dataset.initialY);

		// Calculate the center position of the overlay
		const centerX = initialX + overlay.offsetWidth / 2 * panzoom_inverted_scale;
		const centerY = initialY + overlay.offsetHeight / 2 * panzoom_inverted_scale;

		// Adjust the position to account for the scaling
		const adjustedX = centerX - (overlay.offsetWidth / 2 * panzoom_inverted_scale);
		const adjustedY = centerY - (overlay.offsetHeight / 2 * panzoom_inverted_scale);

		const rotation = overlay.dataset.initialRotation;

		// Apply the new transform
		overlay.style.transform = `translate(${adjustedX}px, ${adjustedY}px) scale(${panzoom_inverted_scale}) rotate(${rotation}deg)`;

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
	if (!map_markers)
		return;

	for (let i = 0; i < map_markers.length; i++) {
		let marker = map_markers[i];

		switch (marker.type) {
			case markers.PLAYER:
				createMarker.createPlayerMarker(i, marker); break;
			case markers.EXPLOSION:
				createMarker.createExplosionMarker(i, marker); break;
			case markers.SHOP:
				createMarker.createShopMarker(i, marker); break;
			case markers.CHINOOK:
				createMarker.createChinookMarker(i, marker); break;
			case markers.CARGO:
				createMarker.createCargoMarker(i, marker); break;
			case markers.CRATE:
				createMarker.createCrateMarker(i, marker); break;
			case markers.RADIUS:
				createMarker.createRadiusMarker(i, marker); break;
			case markers.HELI:
				createMarker.createHeliMarker(i, marker); break;
			default:
				log("Cannot create marker of type: " + marker.type);
		}
	}
}

export function scaledDim(num) {
	return String(num * (server.size / 3000)) + "px"
}

function getMapImageWhitespace() {
	const panzoomElement = document.getElementById('panzoom-element');
	const mapImage = document.getElementById('map-image');

	if (panzoomElement && mapImage) {
		// Get the aspect ratio of the panzoom container
		const panzoomRect = panzoomElement.getBoundingClientRect();
		const panzoomAspectRatio = panzoomRect.width / panzoomRect.height;

		// Get the natural aspect ratio of the map image
		const mapImageAspectRatio = mapImage.naturalWidth / mapImage.naturalHeight;

		// Check if the container's aspect ratio is wider than the image's
		if (panzoomAspectRatio > mapImageAspectRatio) {
			// Calculate the width the image would have if it filled the height of the container
			const imageWidthIfFullHeight = panzoomRect.height * mapImageAspectRatio;

			// The difference in width is the total whitespace, which we halve for one side
			const whitespaceWidth = (panzoomRect.width - imageWidthIfFullHeight) / 2;

			return whitespaceWidth;
		}
	}

	return 0; // No whitespace or elements not found
}



function log(...args) {
	if (DEBUG)
		console.log("%c[map.js] ", "color: #E74C3C", ...args);
}