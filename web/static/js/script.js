$(document).ready(function () {
  $(".command-btn").click(function () {
    if ($(this).hasClass("toggleable")) {
      $(this).toggleClass("active inactive");
    }
  });
});
// Add to your existing script.js file or inline script tag

$(document).ready(function () {
  console.log("X");
  $(".command-btn").click(function () {
    if ($(this).hasClass("modal-trigger")) {
      $("#commandModal").modal("show");
      // Set the title or content of the modal based on the command
      $("#commandModalLabel").text(`Options for ${$(this).text()}`);
    }
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
  const scale = panzoom.getScale();

  adjustOverlayPositionZoom("overlay1", scale);
  adjustOverlayPositionZoom("overlay2", scale);
}

function adjustOverlayPositionZoom(overlayId, scale) {
  const overlay = document.getElementById(overlayId);
  if (overlay) {
    // Retrieve initial positions from dataset
    const initialX = parseFloat(overlay.dataset.initialX);
    const initialY = parseFloat(overlay.dataset.initialY);

    // We just have to scale by this
    const invertedScale = 1 / scale;

    overlay.style.transform = `translate(${initialX}px, ${initialY}px) scale(${invertedScale})`;
  }
}
