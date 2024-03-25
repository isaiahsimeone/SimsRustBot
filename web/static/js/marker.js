import { leaflet_map_markers } from "./map.js";
import { Marker } from "./structures.js";
import { nameFromSteamId, steamImageExists } from "./steam.js";



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

/**
 * Create a player marker and add it to the leaflet map
 * @param {Marker} player - The playermarker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createPlayerMarker(player, scale) {

    var playerIcon = L.icon({
        iconUrl: "static/images/rust/player.png",
        iconSize: [15, 15],
        iconAnchor: [7.5, 7.5],
        popupAnchor: [0, -20]
    });

    if (steamImageExists(player.steam_id)) {
        console.log("exists. yes");

        playerIcon = L.icon({
            iconUrl: "static/images/steam_pics/" + player.steam_id + ".png",
            iconSize: [15, 15],
            iconAnchor: [7.5, 7.5],
            popupAnchor: [0, -20]
        });
    }
    L.marker([player.y * scale, player.x * scale], {icon: playerIcon}).addTo(leaflet_map_markers);
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
    let x = marker.x;
    let y = marker.y;

    if (marker.out_of_stock)
        L.marker([y * scale, x * scale], {icon: shopOutOfStockIcon}).addTo(leaflet_map_markers);
    else
        L.marker([y * scale, x * scale], {icon: shopInStockIcon}).addTo(leaflet_map_markers);
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

}

/**
 * Create a crate marker and add it to the leaflet map 
 * Currently disabled in rust+ (15/03/2024)
 * @param {Marker} marker - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createCrateMarker(marker, scale) {

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


export function deleteAllMapMarkers() {
    leaflet_map_markers.clearLayers();
}