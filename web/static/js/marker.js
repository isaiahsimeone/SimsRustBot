import { map_markers } from "./map.js";
import { Marker } from "./structures.js";
import { steamImageExists } from "./steam.js";

var shopInStockIcon = L.icon({
    iconUrl: "static/images/rust/shop_green.png",
    iconSize: [15, 15],
    iconAnchor: [7.5, 7.5],
    popupAnchor: [0, -25]
});

var shopOutOfStockIcon = L.icon({
    iconUrl: "static/images/rust/shop_orange.png",
    iconSize: [15, 15],
    iconAnchor: [7.5, 7.5],
    popupAnchor: [0, -25]
});

var cargoShipIcon = L.icon({
    iconUrl: "static/images/rust/cargo_ship_body.png",
    iconSize: [40, 40],
    iconAnchor: [20, 20],
    popupAnchor: [0, -25]
});

var crateIcon = L.icon({
    iconUrl: "static/images/rust/crate.png",
    iconSize: [15, 15],
    iconAnchor: [7.5, 7.5],
    popupAnchor: [0, -25]
});

/**
 * Create a player marker and add it to the leaflet map
 * @param {Marker} player - The playermarker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createPlayerMarker(player, scale) {
    const iconImg = steamImageExists(player.steam_id) ? player.steam_id : "default";

    var playerIcon = L.icon({
        iconUrl: "static/images/steam_pics/" + iconImg + ".png",
        iconSize: [20, 20],
        iconAnchor: [10, 10],
        popupAnchor: [0, -20],
        className: "circular-icon"
    });
    var marker = L.marker([player.y * scale, player.x * scale], {icon: playerIcon}).addTo(map_markers);
    marker.marker = player;
    return marker
}

/**
 * Create an explosion marker and add it to the leaflet map
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createExplosionMarker(marker, scale) {
}

/**
 * Create a vending machine shop marker and add it to the leaflet map
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createShopMarker(marker, scale) {
    var m;
    if (marker.out_of_stock)
        m = L.marker([marker.y * scale, marker.x * scale], {marker: marker, icon: shopOutOfStockIcon}).addTo(map_markers);
    else
        m = L.marker([marker.y * scale, marker.x * scale], {marker: marker, icon: shopInStockIcon}).addTo(map_markers);
    m.marker = marker;
    return m;
}

/**
 * Create a chinook marker and add it to the leaflet map
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createChinookMarker(marker, scale) {

}

/**
 * Create a cargo ship marker and add it to the leaflet map
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createCargoMarker(marker, scale) {
    console.log("ROT", marker.rotation);
    return L.marker([marker.y * scale, marker.x * scale], {
        icon: cargoShipIcon,
        rotationAngle: 360 - marker.rotation
    }).addTo(map_markers);
}

/**
 * Create a crate marker and add it to the leaflet map 
 * Currently disabled in rust+ (15/03/2024)
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createCrateMarker(marker, scale) {
    return L.marker([y * scale, x * scale], {icon: crateIcon}).addTo(map_markers);
}

/**
 * I don't know what a radius marker is, but the API supports it
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createRadiusMarker(marker, scale) {

}

/**
 * Create an attack helicopter marker and add it to the leaflet map
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createHeliMarker(marker, scale) {

}
