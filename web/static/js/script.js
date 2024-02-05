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


function setOverlayImage(overlayId, imagePath, initialX, initialY) {
  const overlay = document.getElementById(overlayId);
  if (overlay) {
    overlay.style.backgroundImage = `url('${imagePath}')`;
    overlay.style.transform = `translate(${initialX}px, ${initialY}px)`;
    overlay.style.display = "block"; // Show the overlay
    // Store initial positions
    overlay.dataset.initialX = initialX;
    overlay.dataset.initialY = initialY;
  }
}

function adjustOverlaysOnZoom(panzoom) {
  const panzoom_scale = panzoom.getScale();
  const client_scale = window.devicePixelRatio;

  const overlays = document.getElementsByClassName("overlay")
  for (var i = 0; i < overlays.length; i++) {
    adjustOverlayPositionZoom(overlays[i].id, panzoom_scale, client_scale);
  }
  //adjustOverlayPositionZoom("overlay100", scale);
  //adjustOverlayPositionZoom("overlay200", scale);
}

function adjustOverlayPositionZoom(overlayId, panzoom_scale, client_scale) {
  const overlay = document.getElementById(overlayId);
  if (overlay) {
    // We just have to scale by this?
    const invertedScale = (1 / panzoom_scale) * (1 / client_scale);
    
    // Retrieve initial positions from dataset
    const initialX = parseFloat(overlay.dataset.initialX * (1 / client_scale));
    const initialY = parseFloat(overlay.dataset.initialY * (1 / client_scale));

    overlay.style.transform = `translate(${initialX}px, ${initialY}px) scale(${invertedScale})`;
  }
}

function updateMapMarkers(data) {
  // Logic to update map markers on the map
  //console.log("Update map with markers:", data);

  map_img = document.getElementById("map-image");
  console.log(map_img.width + " " + map_img.height);

  const MAP_WIDTH = 1000;
  const MAP_HEIGHT = 1000;

  const scale_x = 1280 / MAP_WIDTH;
  const scale_y = 945 / MAP_HEIGHT; 

  for (var i = 0; i < data.length; i++) {
    // Add new element to dom
    if (data[i].type != 1)
      continue;
    const overlay = document.createElement("div")
    overlay.className = "overlay";
    overlay.id = "overlay" + i;
    //<div class="overlay" id="overlay100"></div>
    document.getElementById("map-container").appendChild(overlay)

    map_point_x = scale_x * data[i].x - data[i].x * 0.07;//1500 + 880;
    map_point_y = 945 - (data[i].y * scale_y);//1500 - 1350;    

    //console.log("ADD: " + overlay.id, "static/images/rust/crate.png", data[i].x, data[i].y)
    setOverlayImage(overlay.id, "static/images/rust/crate.png", map_point_x, map_point_y);
  }
}
