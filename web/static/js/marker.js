import { scaledDim, setMarkerImage, positionMarker, markers, panzoom_inverted_scale } from "./map.js";
import { steamPictureOrDefault, nameFromSteamId } from "./steam.js";
import { applyRotation } from "./util.js";

const DEBUG = false;

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

function createOverlay(id) {
    let overlay = document.createElement("div");
    overlay.className = "overlay";
    overlay.id = id;
    return overlay;
}

export function createPlayerMarker(id, marker) {
    let overlay = createOverlay(id);

    overlay.style.zIndex = 4; // Always on top				
    overlay.style.width = scaledDim(21);
    overlay.style.height = scaledDim(21);
    overlay.classList.add("circle-image");
    overlay.classList.add ("player");
    overlay.dataset.is_player = true;
    let img = steamPictureOrDefault(marker.steam_id);

	document.getElementById("map-container").appendChild(overlay);  // Move
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker.x, marker.y);

    log("Created player marker ID=", overlay.id, ", X=", marker.x, ", Y=", marker.y, ", img=", img);
}

export function createExplosionMarker(id, marker_xy) {
    let overlay = createOverlay(id);

    overlay.style.width = scaledDim(12);
    overlay.style.height = scaledDim(12);
    let img = marker_type_to_img[markers.EXPLOSION];

	document.getElementById("map-container").appendChild(overlay);
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker_xy.x, marker_xy.y);

    log("Created explosion marker ID=", overlay.id, "X=", marker_xy.x, "Y=", marker_xy.y);
}

export function createShopMarker(id, marker) {
    let overlay = createOverlay(id);
			
    overlay.style.width = scaledDim(12);
    overlay.style.height = scaledDim(12);
    let img = marker.out_of_stock ? marker_type_to_img[markers.SHOP][1] : marker_type_to_img[markers.SHOP][0];

	document.getElementById("map-container").appendChild(overlay);  // Move
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker.x, marker.y);

    log("Created shop marker ID=", overlay.id, "X=", marker.x, "Y=", marker.y, "img=", img, "out_of_stock=", marker.out_of_stock);
}

export function createChinookMarker(id, marker) {
    let overlay = createOverlay(id);

    overlay.style.width = scaledDim(35);
    overlay.style.height = scaledDim(35);
    let img = marker_type_to_img[markers.CHINOOK][0];

    var theta = (360 - marker.rotation) * Math.PI / 180;
    var magnitude = parseInt(overlay.style.width.replace("px","")) * (panzoom_inverted_scale) * 1.1;
    var blade_x = magnitude * Math.sin(theta);
    var blade_y = magnitude * Math.cos(theta);
    
    // Draw blades
    drawBlades("overlay" + id + "blades", marker_type_to_img[markers.CHINOOK][1], marker.x + blade_x, marker.y + blade_y);
    drawBlades("overlay" + id + "blades2", marker_type_to_img[markers.CHINOOK][1], marker.x - blade_x, marker.y - blade_y);

    document.getElementById("map-container").appendChild(overlay);  // Move
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker.x, marker.y, 360 - marker.rotation);

    log("Created chinook marker ID=", overlay.id, "X=", marker.x, "Y=", marker.y, "Rot=", 360 - marker.rotation, "img=", img);
}

export function createCargoMarker(id, marker) {
    let overlay = createOverlay(id);

    overlay.style.width = scaledDim(50);
    overlay.style.height = scaledDim(50);
    let img = marker_type_to_img[markers.CARGO];

	document.getElementById("map-container").appendChild(overlay);  // Move
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker.x, marker.y, 360 - marker.rotation);

    log("Created cargo marker ID=", overlay.id, "X=", marker.x, "Y=", marker.y, "Rot=", 360 - marker.rotation, "img=", img);

}

export function createRadiusMarker(id, marker) {
    // I don't know what this is
}

export function createCrateMarker(id, marker) {
    // No longer provided by rust plus API (19/02/2024)
}

export function createHeliMarker(id, marker) {
    let overlay = createOverlay(id);

    overlay.style.width = scaledDim(35);
    overlay.style.height = scaledDim(35);
    let img = marker_type_to_img[markers.HELI][0];

    
    var theta = (360 - marker.rotation) * Math.PI / 180;
    var magnitude = parseInt(overlay.style.width.replace("px","")) * (panzoom_inverted_scale) * 0.7;
    var blade_x = magnitude * Math.sin(theta);
    var blade_y = magnitude * Math.cos(theta);

    // Draw blades
    drawBlades("overlay" + id + "blades", marker_type_to_img[markers.HELI][1], marker.x + blade_x, marker.y + blade_y);

    document.getElementById("map-container").appendChild(overlay);  // Move
	setMarkerImage(overlay.id, img);
	positionMarker(overlay.id, marker.x, marker.y, 360 - marker.rotation);

    log("Created heli marker ID=", overlay.id, "X=", marker.x, "Y=", marker.y, "Rot=", 360 - marker.rotation, "img=", img);
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
	setMarkerImage(overlayId, img);
	positionMarker(overlayId, x, y, 0);
}

function log(...args) {
	if (DEBUG)
        console.log("%c[marker.js] ", "color: #00FFFF", ...args);
}
