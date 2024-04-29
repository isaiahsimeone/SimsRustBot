import { map_markers, leaflet_shop_markers, scale, player_markers, leaflet_custom_map_notes } from "./map.js";
import { Marker } from "./structures.js";
import { steamImageExists } from "./steam.js";
import * as map_notes from "./map_notes.js";
import * as util from "./util.js";

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
 */
export function createPlayerMarker(player) {
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
    
    if (iconImg !== "default")
        marker.image_loaded = true;

    marker.marker = player;

    player_markers.set(player.steam_id, marker);
    
    return marker
}

/**
 * Create an explosion marker and add it to the leaflet map
 * @param {Marker} explosion - The marker object to plot on the map
 */
export function createExplosionMarker(explosion) {
    console.log("explosion plotted", explosion);
    var marker = L.marker([explosion.y * scale, explosion.x * scale], {icon: explosionIcon}).addTo(map_markers);
    marker.marker = explosion;
    return marker;
}

/**
 * Create a vending machine shop marker and add it to the leaflet map
 * @param {Marker} shop - The marker object to plot on the map
 */
export function createShopMarker(shop) {
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
 */
export function createChinookMarker(chinook) {
    var marker = L.marker([chinook.y * scale, chinook.x * scale], { icon: chinookIcon, rotationAngle: 360 - chinook.rotation }).addTo(map_markers);
    marker.marker = chinook;
    return marker;
}

/**
 * Create a cargo ship marker and add it to the leaflet map
 * @param {Marker} cargo - The marker object to plot on the map
 */
export function createCargoMarker(cargo) {
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
 */
export function createCrateMarker(crate) {
    var marker = L.marker([crate.y * scale, crate.x * scale], {icon: crateIcon}).addTo(map_markers);
    marker.marker = crate;
    return marker;
}

/**
 * I don't know what a radius marker is, but the API supports it
 * @param {Marker} radius - The marker object to plot on the map
 */
export function createRadiusMarker(radius) {

}

/**
 * Create an attack helicopter marker and add it to the leaflet map
 * @param {Marker} heli - The marker object to plot on the map
 */
export function createHeliMarker(heli) {
    var marker = L.marker([heli.y * scale, heli.x * scale], { icon: attackHelicopterIcon, rotationAngle: 360 - heli.rotation }).addTo(map_markers);
    marker.marker = heli;
    return marker;
}

export function createNoteMarker(extended_note) {
    var note = extended_note.note;
    var creator_steam_id = extended_note.steam_id;

    var selected_colour = map_notes.MapNoteColours[note.colour_index];
    var background_colour = util.darkenRGB(selected_colour);
    var icon_index = note.icon;
    var label = note.label;

    var noteIcon = L.divIcon({
        html: `
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 22px; height: 22px; position: relative; display: flex; justify-content: center; align-items: center;">
                    <div class="note-background" style="background-color: ${background_colour}; position: absolute; width: 100%; height: 100%;">
                    </div>
                    <div class="note-mask" style="mask: url('static/images/markers/${icon_index}.png') center center / 60% no-repeat; background-color: ${selected_colour}; position: absolute; width: 100%; height: 100%;">
                    </div>
                    <div class="note-border" style="border: 1px solid ${selected_colour}; position: absolute; width: 101%; height: 101%;">
                    </div>
                </div>
            <div class="note-text">${label}</div>
        </div>`,
        iconSize: [20, 60], 
        iconAnchor: [10, 30], 
        className: '' // Avoid leaflet's default icon styling
    });

    var marker = L.marker([parseInt(note.y) * scale, parseInt(note.x) * scale], { icon: noteIcon }).addTo(leaflet_custom_map_notes);
    marker.creation_time = util.timeNow();
    marker.steam_id = creator_steam_id;
    return marker;
}