
// Global variables
const mapImage = document.getElementById('map-image');
let initialMapRect = null;
let map_image_offset_left = getMapImageWhitespace();
let map_marker_data = null;

// Set the first time json data is received
let MAP_SZ = null;

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
		const panzoom = Panzoom(panzoomElement, {
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
function setOverlayImage(overlayId, imagePath, jsonX, jsonY, panzoom) {
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
	overlay.style.backgroundImage = `url('${imagePath}')`;
	overlay.style.transform = `translate(${imageX}px, ${imageY}px) scale(${invertedScale})`;
	overlay.style.display = 'block'; // Show the overlay

	// Store the initial positions
	overlay.dataset.initialX = imageX;
	overlay.dataset.initialY = imageY;
}

// Adjust overlays on zoom
function adjustOverlaysOnZoom(panzoom) {
	const panzoomScale = panzoom.getScale();
	const clientScale = window.devicePixelRatio;
	const overlays = document.getElementsByClassName("overlay");

	for (let i = 0; i < overlays.length; i++) {
		adjustOverlayPositionZoom(overlays[i].id, panzoomScale, clientScale);
	}
}

// Adjust individual overlay position
function adjustOverlayPositionZoom(overlayId, panzoom_scale) {
	const overlay = document.getElementById(overlayId);
	if (overlay) {
		// Overlay size changes depending on panzoom scale
		const invertedScale = 1 / panzoom_scale;

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

// Update map markers
function updateMapMarkers(data, panzoom) {
	for (let i = 0; i < data.length; i++) {
		if (data[i].type !== 1) continue;

		const overlay = document.createElement("div");
		overlay.className = "overlay";
		overlay.id = "overlay" + i;
		document.getElementById("map-container").appendChild(overlay);

		setOverlayImage(overlay.id, "static/images/rust/player.png", data[i].x, data[i].y, panzoom);
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
  