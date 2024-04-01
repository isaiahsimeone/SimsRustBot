import { map_markers, leaflet_shop_markers } from "./map.js";
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

var explosionIcon = L.icon({
    iconUrl: "static/images/rust/explosion.png",
    iconSize: [15, 15],
    iconAnchor: [7.5, 7.5],
    popupAnchor: [0, -25]
});

var attackHelicopterIcon = L.divIcon({
    html: `
      <div class="helicopter-marker">
        <img src="static/images/rust/heli_map_body.png">
        <div class="helicopter-blades">
          <img src="static/images/rust/map_blades.png">
        </div>
      </div>`,
    iconSize: [40, 40], 
    iconAnchor: [20, 20],
    className: '' // Avoid leaflet's default icon styling
});

var chinookIcon = L.divIcon({
    html: `
      <div class="helicopter-marker">
        <img src="static/images/rust/chinook_map_body.png">
        <div class="chinook-blades-front">
            <img src="static/images/rust/map_blades.png">
        </div>
        <div class="chinook-blades-back">
            <img src="static/images/rust/map_blades.png">
        </div>
      </div>`,
    iconSize: [35, 35],
    iconAnchor: [17.5, 17.5],
    className: '' // Avoid leaflet's default icon styling
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
        zIndexOffset: 100,
        className: "circular-icon"
    });

    var marker = L.marker([player.y * scale, player.x * scale], {icon: playerIcon}).addTo(map_markers);
    
    if (iconImg !== "default") {
        console.log("image loaded set");
        marker.image_loaded = true;
    }

    marker.marker = player;
    
    return marker
}

/**
 * Create an explosion marker and add it to the leaflet map
 * @param {Marker} explosion - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createExplosionMarker(explosion, scale) {
    console.log("explosion plotted", explosion);
    var marker = L.marker([explosion.y * scale, explosion.x * scale], {icon: explosionIcon}).addTo(map_markers);
    marker.marker = explosion;
    return marker;
}

/**
 * Create a vending machine shop marker and add it to the leaflet map
 * @param {Marker} shop - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createShopMarker(shop, scale) {
    var marker;
    if (shop.out_of_stock)
        marker = L.marker([shop.y * scale, shop.x * scale], {marker: shop, icon: shopOutOfStockIcon}).addTo(leaflet_shop_markers);
    else
        marker = L.marker([shop.y * scale, shop.x * scale], {marker: shop, icon: shopInStockIcon}).addTo(leaflet_shop_markers);
    marker.marker = shop;
    return marker;
}

/**
 * Create a chinook marker and add it to the leaflet map
 * @param {Marker} chinook - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createChinookMarker(chinook, scale) {
    var marker = L.marker([chinook.y * scale, chinook.x * scale], { icon: chinookIcon, rotationAngle: 360 - chinook.rotation }).addTo(map_markers);
    marker.marker = chinook;
    return marker;
}

/**
 * Create a cargo ship marker and add it to the leaflet map
 * @param {Marker} cargo - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createCargoMarker(cargo, scale) {
    var marker = L.marker([cargo.y * scale, cargo.x * scale], {
        icon: cargoShipIcon,
        rotationAngle: 360 - cargo.rotation
    }).addTo(map_markers);
    marker.marker = cargo;
    return marker;
}

/**
 * Create a crate marker and add it to the leaflet map 
 * Currently disabled in rust+ (15/03/2024)
 * @param {Marker} crate - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createCrateMarker(crate, scale) {
    var marker = L.marker([crate.y * scale, crate.x * scale], {icon: crateIcon}).addTo(map_markers);
    marker.marker = crate;
    return marker;
}

/**
 * I don't know what a radius marker is, but the API supports it
 * @param {Marker} radius - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createRadiusMarker(radius, scale) {

}

/**
 * Create an attack helicopter marker and add it to the leaflet map
 * @param {Marker} heli - The marker object to plot on the map
 * @param {float} scale - The amount to scale the marker coordinates by
 */
export function createHeliMarker(heli, scale) {
    var marker = L.marker([heli.y * scale, heli.x * scale], { icon: attackHelicopterIcon, rotationAngle: 360 - heli.rotation }).addTo(map_markers);
    marker.marker = heli;
    return marker;
}
