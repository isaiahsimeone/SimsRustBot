
// Global variables
const mapImage = document.getElementById("map-image");
const mapContainer = document.getElementById("map-container")
let panzoom = null;
let initialMapRect = null;
let img_path = "static/images";

let map_image_offset_left = getMapImageWhitespace();

let map_marker_data = null;
let map_monument_data = null;
let server_info_data = null
let team_info = null;

let steam_images_available = [];

let map_markers_ES = null;
let team_updates_ES = null;
let ES_reset_count = 0;


// RustInfo[url=, name=Sims Server, map=Procedural Map, size=4000, players=0, max_players=5, queued_players=0, seed=793197, wipe_time=1707127438, header_image=, logo_image=]

// TODO: when heli/cargo is coming in, specify the direction that the player can align their compass to. Just a vector

let MAP_SZ = null;

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
	/* 0 */ [/* no image */],
	/* 1 */ ["player.png"],
	/* 2 */ ["explosion.png"],
	/* 3 */ ["shop_green.png", "shop_orange.png"],
	/* 4 */ ["chinook_map_body.png", "map_blades.png"],
	/* 5 */ ["cargo_ship_body.png"],
	/* 6 */ ["crate.png"],
	/* 7 */ [/* Radius marker, i don't know what this is? */],
	/* 8 */ ["heli_map_body.png", "map_blades.png"]
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



// Document ready functions
$(document).ready(function() {
	// Command button functionality
	$('.command-btn').click(function() {
		if ($(this).hasClass('toggleable')) {
			$(this).toggleClass('active inactive');
		}
		if ($(this).hasClass('modal-trigger')) {
			$('#commandModal').modal('show');
			$('#commandModalLabel').text(`Options for ${$(this).text()}`);
		}
	})

	// Click event on map image
	$('#map-image').click(function(e) {
		var offset_t = $(this).offset().top - $(window).scrollTop();
		var offset_l = $(this).offset().left - $(window).scrollLeft();
		var left = Math.round(e.clientX - offset_l);
		var top = Math.round(e.clientY - offset_t);
		console.log('Left: ' + left + ' Top: ' + top);
	});

	// Initialize map image rect
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

		$(window).on('resize', function() {
			console.log(window.devicePixelRatio);
			map_image_offset_left = getMapImageWhitespace();
			updateInitialMapRect();
			updateMapMarkers(map_marker_data);
			redrawMonuments();
			adjustOverlaysOnZoom();
		});

		// Listen to Zoom events
		panzoomElement.addEventListener('panzoomzoom', function() {
			updateMapMarkers(map_marker_data);
			adjustOverlaysOnZoom();
		});
		// This part runs once - we need map_sz set first
		$.getJSON(window.location.href + 'serverinfo', function(data) {
			getServerInfo(data.data);
		});

		$.getJSON(window.location.href + 'monuments', function(data) {
			getMapMonuments(data.data);
		});
		
		$.getJSON(window.location.href + 'teaminfo', function(data) {
			team_info = data.data;
			
			for (let i = 0; i < team_info.members.length; i++) {
				downloadSteamImage(String(team_info.members[i].steam_id));
				console.log(team_info.members[i]);
			}
			console.log("got team info: " + Object.keys(team_info));
			console.log(team_info.map_notes);
		});

		if (!!window.EventSource) {
			resetEventSource();			
		}
	}

});


function resetEventSource() {
    if (map_markers_ES) {
		console.log("reset marker ES");
        map_markers_ES.close();
    }
    if (team_updates_ES) {
		console.log("reset update ES");
        team_updates_ES.close();
    }
    
    // Reinitialize the EventSource
    map_markers_ES = new EventSource('/markers');
    team_updates_ES = new EventSource('/teammemberupdates');
    map_markers_ES.addEventListener('message', getMapMarkersFromES, false);
    team_updates_ES.addEventListener('message', getTeamUpdateFromES, false);

	ES_reset_count = 0;
}

function getTeamUpdateFromES(data) {
	console.log(data.data);
}

function getServerInfo(data) {
	console.log("SERVER INFO keys: " + Object.keys(data));
	server_info_data = data;
	// Get map size
	let map_size = data.size
	MAP_SZ = map_size;
	console.log("Map size is " + MAP_SZ);
}

function steamPictureOrDefault(steam_id) {
	if (steamImageExists(steam_id))
		return steam_id;
	return "default";
}

function steamImageExists(steam_id) {
	console.log(steam_images_available.includes(steam_id));
	return steam_images_available.includes(steam_id);
}

function downloadSteamImage(steamId) {
	console.log("downloading " + String(steamId));
	const url = `${window.location.href}downloadsteamimage/${steamId}`;
	
	fetch(url, {
	  method: 'POST',
	})
	  .then(response => response.json()) // Assuming JSON response
	  .then(data => {
		if (data.success) {
		  // Image processing started, now poll for availability or proceed as necessary
		  console.log(data.message);
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

function createMapText(id, x, y, text) {
	let text_overlay = document.createElement("div");
	text_overlay.className = "overlay map_text";
	text_overlay.id = "overlay_text" + id;

	text_overlay.style.fontSize = "10px";
	text_overlay.innerHTML = text;

	mapContainer.appendChild(text_overlay);

	setOverlay(text_overlay.id, x, y, 0);
}

function getMapMarkersFromES(marker_data) {
	
	//console.log('Received data: ', marker_data.data);
	deleteAllMapMarkers(); // Remove current overlays from DOM
	map_marker_data = JSON.parse(marker_data.data);
	//console.log(map_marker_data);
	updateMapMarkers();

	if (ES_reset_count++ > 200)
		resetEventSource();
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
				overlay_img = steamPictureOrDefault(marker.steam_id)
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
	return String(num * (MAP_SZ / 3000)) + "px"
}


  
function applyRotation(elementId) {
    let angle = Math.ceil(Math.random() * 360); // Initial angle

    // Function to update rotation
    function update() {
        angle = (angle + 1) % 360; // Increment angle and loop at 360
        const element = document.getElementById(elementId);
        if (element) {
            // Combine rotation with existing transform, preserving position and scale
            const transform = element.style.transform;
            const rotateTransform = `rotate(${angle}deg)`;
            element.style.transform = transform.replace(/rotate\([0-9]+deg\)/, '') + ' ' + rotateTransform;
        }
        requestAnimationFrame(update); // Continue rotation
    }

    update(); // Start rotation
}