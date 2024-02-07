
// Global variables
const mapImage = document.getElementById('map-image');
let panzoom = null;
let initialMapRect = null;
let map_image_offset_left = getMapImageWhitespace();
let map_marker_data = null;

// Set the first time json data is received
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
		console.log("DEVICE: " + window.devicePixelRatio);
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
			updateMapMarkers(map_marker_data, panzoom);
			adjustOverlaysOnZoom(panzoom);
		});

		// Listen to Zoom events
		panzoomElement.addEventListener('panzoomzoom', function() {
			adjustOverlaysOnZoom(panzoom);
		});

		if (!!window.EventSource) {
			var source = new EventSource('/stream');

			source.addEventListener(
				'message',
				function(e) {
					console.log('Received data: ', e.data);
					deleteAllMapMarkers(); // Remove current overlays from DOM
					map_marker_data = JSON.parse(e.data);
					if (MAP_SZ == null) {
						console.log("map size = " + map_marker_data[0]);
						MAP_SZ = map_marker_data[0];
					}
					updateMapMarkers(map_marker_data, panzoom);
				},
				false
			);
		}
	}
});

function updateInitialMapRect() {
	if (mapImage) {
		initialMapRect = mapImage.getBoundingClientRect();
	}
}

// places an overlay image on the map given JSON coordinates
// from the RustAPI. It will be converted to coordinates suitable
// for the map image displayed in browser
function setOverlayImage(overlayId, imagePath, jsonX, jsonY, rotation) {
	const overlay = document.getElementById(overlayId);
	console.log("ROTATION: " + rotation);

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
	overlay.style.backgroundImage = `url('${imagePath}')`;
	overlay.style.transform = `translate(${imageX}px, ${imageY}px) scale(${invertedScale}) rotate(${rotation}deg)`;
	overlay.style.display = 'block'; // Show the overlay

	// Store the initial positions
	overlay.dataset.initialX = imageX;
	overlay.dataset.initialY = imageY;
}

// Adjust overlays on zoom
function adjustOverlaysOnZoom() {
	const overlays = document.getElementsByClassName("overlay");

	for (let i = 0; i < overlays.length; i++) {
		adjustOverlayPositionZoom(overlays[i].id, panzoom.getScale());
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

		// Apply the new transform
		overlay.style.transform = `translate(${adjustedX}px, ${adjustedY}px) scale(${invertedScale})`;
	}
}

function deleteAllMapMarkers() {
	var elements = document.getElementsByClassName("overlay");

	Array.from(elements).forEach((element) => {
	  element.remove(); // Removes the element from the DOM
	});
}

// Update map markers
function updateMapMarkers() {

	for (let i = 1; i < map_marker_data.length; i++) {
		let overlay_img = null;
		let marker = map_marker_data[i];
		let marker_type = marker.type;

		const overlay = document.createElement("div");
		overlay_img = marker_type_to_img[marker_type]; // May change in switch

		switch (marker_type) {
			case markers.PLAYER:
				overlay.style.zIndex = 1; // Always on top
				break;
			case markers.SHOP:
				overlay_img = marker.out_of_stock ? marker_type_to_img[markers.SHOP][1] : marker_type_to_img[markers.SHOP][0];
				overlay.style.width = "12px";
				overlay.style.height = "12px";
				break;
			case markers.CHINOOK:
				overlay_img = marker_type_to_img[markers.CHINOOK][0];
				// Rotate

				// Draw blade

				break;
			case markers.CARGO:
				overlay.style.width = "35px";
				overlay.style.height = "35px";
				// Rotate

				break;
			case markers.HELI:
				overlay_img = marker_type_to_img[markers.HELI][0];
				// Rotate

				// Draw blades

				break;
		}
	
		let rotation = 360 - map_marker_data[i].rotation;

		overlay.className = "overlay";
		overlay.id = "overlay" + i;
		document.getElementById("map-container").appendChild(overlay);

		setOverlayImage(overlay.id, "static/images/rust/" + overlay_img, map_marker_data[i].x, map_marker_data[i].y, rotation);
	}
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
  