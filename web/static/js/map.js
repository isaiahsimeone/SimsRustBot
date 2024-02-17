import { server } from "./server.js";
import { applyRotation } from "./util.js";
import { img_path } from "./main.js";
import { steamPictureOrDefault, nameFromSteamId } from "./steam.js";
import * as socketio from "./socketio.js";

const DEBUG = true;

const mapImage = document.getElementById("map-image");
const mapContainer = document.getElementById("map-container")

let panzoom = null;
let map_image_offset_left = 0;
let initial_map_rect = null;
let server_to_browser_scale = null;

let map_markers = null;
let map_monuments = null;

const markers = {
    PLAYER: 1,
    EXPLOSION: 2,
    SHOP: 3,
    CHINOOK: 4,
    CARGO: 5,
    CRATE: 6,
    RADIUS: 7,
    HELI: 8
};

const marker_type_to_img = [
	/* 0 */[/* no image */],
	/* 1 */["player.png"],
	/* 2 */["explosion.png"],
	/* 3 */["shop_green.png", "shop_orange.png"],
	/* 4 */["chinook_map_body.png", "map_blades.png"],
	/* 5 */["cargo_ship_body.png"],
	/* 6 */["crate.png"],
	/* 7 */[/* Radius marker, i don't know what this is? */],
	/* 8 */["heli_map_body.png", "map_blades.png"]
];


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
            map_image_offset_left = getMapImageWhitespace();
            updateInitialMapRect();
            updateMapMarkers();
            redrawMonuments();
            adjustOverlaysOnZoom();
        });

        // Listen to Zoom events
        panzoomElement.addEventListener('panzoomzoom', function () {
            updateMapMarkers();
            adjustOverlaysOnZoom();
        });
    }
    map_image_offset_left = getMapImageWhitespace();
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

	setOverlay(text_overlay.id, x, y, 0);
}


function updateInitialMapRect() {
	if (mapImage) {
		initial_map_rect = mapImage.getBoundingClientRect();
	}
}


function setOverlay(overlayId, jsonX, jsonY, rotation) {
	
	const overlay = document.getElementById(overlayId);

	if (!overlay || !initial_map_rect)
		return;

	// Overlay dimensions
	const overlay_width = overlay.offsetWidth;
	const overlay_height = overlay.offsetHeight;
	const overlay_width_center = overlay_width / 2;
	const overlay_height_center = overlay_height / 2;


	// position calculations
	const scaleX = initial_map_rect.height / server.size; // I have no idea why we use the image height here, but it works
	const scaleY = initial_map_rect.height / server.size;
	const jsonY_flipped = server.size - jsonY // Flip the Y-coordinate

	// Convert map coordinates (jsonX, jsonY) to image pixel coordinates
	const imageX = scaleX * jsonX + map_image_offset_left - overlay_width_center;
	const imageY = scaleY * jsonY_flipped + initial_map_rect.top - overlay_height_center;
	
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
function setOverlayImage(overlayId, image, is_player=false) {
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
	if (!map_markers)
		return;

	for (let i = 0; i < map_markers.length; i++) {

		let overlay_img = null;
		let marker = map_markers[i];
		let marker_type = marker.type;
		let rotation = 360 - map_markers[i].rotation;

		let x = map_markers[i].x;
		let y = map_markers[i].y;

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
				log(map_markers[i]);
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
				var magnitude = parseInt(overlay.style.width.replace("px","")) * (1 / panzoom.getScale()) * 1.3;
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
				var magnitude = parseInt(overlay.style.width.replace("px","")) * (1 / panzoom.getScale()) * 0.7;
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

function scaledDim(num) {
	return String(num * (server.size / 3000)) + "px"
}


function log(...args) {
    if (DEBUG)
        console.log("[map.js] ", ...args);
}