$(document).ready(function () {
  $(".command-btn").click(function () {
    if ($(this).hasClass("toggleable")) {
      $(this).toggleClass("active inactive");
    }
  });
});


$(document).ready(function () {
  
  $(".command-btn").click(function () {
    if ($(this).hasClass("modal-trigger")) {
      $("#commandModal").modal("show");
      // Set the title or content of the modal based on the command
      $("#commandModalLabel").text(`Options for ${$(this).text()}`);
    }
  });
  $('#map-image').click(function(e)
{   
    var offset_t = $(this).offset().top - $(window).scrollTop();
    var offset_l = $(this).offset().left - $(window).scrollLeft();

    var left = Math.round( (e.clientX - offset_l) );
    var top = Math.round( (e.clientY - offset_t) );

    console.log("Left: " + left + " Top: " + top);

});
});

$(document).ready(function () {
  const mapImage = document.getElementById("map-image");

  if (mapImage) {
    const rect = mapImage.getBoundingClientRect();
    console.log(`Rendered Width: ${rect.width}, Rendered Height: ${rect.height}`);
    console.log(`Position - Top: ${rect.top}, Left: ${rect.left}`);
  }
});

const MAP_WIDTH = 5000;
const MAP_HEIGHT = 5000;

let initialMapRect = null;

$(document).ready(function () {
  // Other code...

  const mapImage = document.getElementById("map-image");
  if (mapImage) {
    // Store the initial dimensions and position of the map image
    initialMapRect = mapImage.getBoundingClientRect();
  }

  // Other code...
});

function setOverlayImage(overlayId, imagePath, mapX, mapY, panzoom) {
  const overlay = document.getElementById(overlayId);

  if (overlay && initialMapRect) {
    // Get the actual size and position of the map image

    const overlay_width = overlay.offsetWidth;
    const overlay_height = overlay.offsetHeight;
    console.log("X : " + initialMapRect.height + " " + initialMapRect.top); 

    // Convert map coordinates (mapX, mapY) to image pixel coordinates
    const imageX = mapX * (initialMapRect.height / MAP_WIDTH) + 166 - overlay_width/2;
  
    const flippedMapY = MAP_HEIGHT - mapY; // Flip the Y-coordinate
    const imageY = (flippedMapY / MAP_HEIGHT) * initialMapRect.height + initialMapRect.top - overlay_height/2;
    
    const invertedScale = 1 / panzoom.getScale();

    // Apply the background image and position the overlay
    overlay.style.backgroundImage = `url('${imagePath}')`;
    overlay.style.transform = `translate(${imageX}px, ${imageY}px) scale(${invertedScale})`;
    overlay.style.display = "block"; // Show the overlay


    if (overlayId == "overlay0")
      console.log("init x,y = + " + imageX + ", " + imageY);

    // Store the initial positions
    overlay.dataset.initialX = imageX; // converts JSON coord to img coord
    overlay.dataset.initialY = imageY;
  }
}

function adjustOverlaysOnZoom(panzoom) {
  const panzoom_scale = panzoom.getScale();
  const client_scale = window.devicePixelRatio;

  const overlays = document.getElementsByClassName("overlay");
  for (var i = 0; i < overlays.length; i++) {
    adjustOverlayPositionZoom(overlays[i].id, panzoom_scale, client_scale);
  }
}

function adjustOverlayPositionZoom(overlayId, panzoom_scale, client_scale) {
  const overlay = document.getElementById(overlayId);
  if (overlay) {
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


function updateMapMarkers(data, panzoom) {
  // Logic to update map markers on the map
  //console.log("Update map with markers:", data);
  invertedScale = 1 / panzoom.getScale();

  map_img = document.getElementById("map-image");
  console.log(map_img.width + " " + map_img.height);

  for (var i = 0; i < data.length; i++) {
    // Add new element to dom
    if (data[i].type != 1)
      continue;
    const overlay = document.createElement("div")
    overlay.className = "overlay";
    overlay.id = "overlay" + i;
    //<div class="overlay" id="overlay100"></div>
    document.getElementById("map-container").appendChild(overlay)

    map_point_x = data[i].x; // this is not right, but close. FOr some reason, the Y doesn't get affected by
    map_point_y = data[i].y;

    //console.log("ADD: " + overlay.id, "static/images/rust/crate.png", data[i].x, data[i].y)
    setOverlayImage(overlay.id, "static/images/rust/player.png", map_point_x, map_point_y, panzoom);
  }
}
