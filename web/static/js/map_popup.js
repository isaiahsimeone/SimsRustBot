

export function bindMarkerPopup(leaflet_marker) {
    var marker = leaflet_marker.marker;
    switch (marker.typeName) {
        case "PLAYER":
            bindPlayerPopup(leaflet_marker);
            break;
        case "EXPLOSION":
            return markerFactory.createExplosionMarker(marker, scale);
        case "SHOP":
            return markerFactory.createShopMarker(marker, scale);
        case "CHINOOK":
            return markerFactory.createChinookMarker(marker, scale);
        case "CARGOSHIP":
            return markerFactory.createCargoMarker(marker, scale);
        case "CRATE":
            return markerFactory.createCrateMarker(marker, scale);
        case "RADIUS":
            return markerFactory.createRadiusMarker(marker, scale);
        case "ATTACKHELI":
            return markerFactory.createHeliMarker(marker, scale);
        default:
            log("Error: Unknown marker type in createMarker()");
    }
}

function bindPlayerPopup(leaflet_marker) {
    var marker = leaflet_marker.marker;

    var popup = "<h3>" + marker.name + "</h3>" + "<p>" + marker.spawn_time + "</p>";

    var opts = {
        maxWidth: "100",
        className: "player-map-popup"
    };

    leaflet_marker.bindPopup(popup, opts);
}