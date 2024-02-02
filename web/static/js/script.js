document.addEventListener("DOMContentLoaded", function() {
    const map = document.getElementById('map');
    let isDragging = false, startX, startY, originalX, originalY, translateX = 0, translateY = 0, scale = 1;

    map.addEventListener('mousedown', function(e) {
        isDragging = true;
        startX = e.pageX - translateX;
        startY = e.pageY - translateY;
    });

    map.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        translateX = e.pageX - startX;
        translateY = e.pageY - startY;
        updateTransform();
    });

    map.addEventListener('mouseup', function(e) {
        isDragging = false;
    });

    map.addEventListener('mouseleave', function(e) {
        isDragging = false;
    });

    map.addEventListener('wheel', function(e) {
        e.preventDefault();
        const deltaScale = Math.sign(e.deltaY) * -0.1;
        scale += deltaScale;
        scale = Math.max(0.5, Math.min(4, scale)); // Limit scale between 0.5 and 4
        updateTransform();
    });

    function updateTransform() {
        map.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }
});
