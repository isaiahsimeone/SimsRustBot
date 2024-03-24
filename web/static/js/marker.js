import { leaflet_map_markers } from "./map.js";
import { serverInfoInstance } from "./server.js";


var playerIcon = L.icon({
    iconUrl: "static/images/rust/player.png",
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, -25]
});

var shopInStockIcon = L.icon({
    iconUrl: "static/images/rust/shop_green.png",
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, -25]
});

var shopOutOfStockIcon = L.icon({
    iconUrl: "static/images/rust/shop_orange.png",
    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, -25]
});


export function createPlayerMarker(x, y, steam_id) {
    L.marker([x, map_sz - y], {icon: playerIcon}).addTo(leaflet_map_markers);
}

export function createExplosionMarker() {

}

export function createShopMarker(x, y, in_stock) {
    if (in_stock)
        L.marker([x, y], {icon: shopInStockIcon}).addTo(leaflet_map_markers);
    else
        L.marker([x, y], {icon: shopOutOfStockIcon}).addTo(leaflet_map_markers);
}

export function createChinookMarker() {

}

export function createCargoMarker() {

}

export function createCrateMarker() {

}

export function createRadiusMarker() {

}

export function createHeliMarker() {

}

export function deleteAllMapMarkers() {
    leaflet_map_markers.clearLayers();
}