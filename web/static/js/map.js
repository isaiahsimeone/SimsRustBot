//@ts-check
import * as socketio from "./socketio.js";
import { Marker, Monument } from "./structures.js";
import * as markerFactory from "./marker.js";
//import { receiveMapNotes } from "./note.js";
//import { receiveTeamMembers } from "./steam.js";
//import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;

/**
 * @type {String}
 */
export let background_colour;

/**
 * @type {Monument[]}
 */
export let monuments = [];

/**
 * @type {Marker[]}
 */
export let markers = [];

export let leaflet_map;

export let leaflet_map_markers;

export let leaflet_monument_names;

/**
 * Get monument and first map marker data from server.
 * After this, map markers will be received every time
 * the server polls for them, they will arrive via socketio
 * broadcast at receiveMarkers()
 */
export async function initialiseMap() {
    // Prepare leaflet
    initLeaflet();

    // Request background colour from server
    background_colour = (await socketio.request_topic("background")).background;
    log("background colour is", background_colour);

    // Request monument data from server
    const monumentData = (await socketio.request_topic("monuments")).monuments;
    log("MONUMENTS:", monumentData);

    for (let i = 0; i < monumentData.length; i++)
        monuments[i] = new Monument(monumentData[i]);
    
    drawMonuments(monumentData);

    // Request first set of map markers from server
    const markerData = (await socketio.request_topic("map_markers")).markers;
    receiveMarkers(markerData);
}

/**
 * 
 * @param {Marker} marker 
 */
function createMarker(marker) {
    log(marker);
    let x = marker.x;
    let y = marker.y;
    switch (marker.typeName) {
        case "PLAYER":
            markerFactory.createPlayerMarker(x, y, marker.steam_id);
            break;
        case "EXPLOSION":
            markerFactory.createExplosionMarker();
            break;
        case "SHOP":
            markerFactory.createShopMarker(x, y, marker.out_of_stock);
            break;
        case "CHINOOK":
            markerFactory.createChinookMarker();
            break;
        case "CARGOSHIP":
            markerFactory.createCargoMarker();
            break;
        case "CRATE":
            markerFactory.createCrateMarker();
            break;
        case "RADIUS":
            markerFactory.createRadiusMarker();
            break;
        case "ATTACKHELI":
            markerFactory.createHeliMarker();
            break;
        default:
            log("Error: Unknown marker type in createMarker()");
    }
}

function initLeaflet() {
    // Initialize Leaflet map with a CRS
    // @ts-ignore
    leaflet_map = L.map('map-container', {
        // @ts-ignore
        crs: L.CRS.Simple,
        minZoom: -1.5,
        zoomControl: false,
        zoomSnap: 0,
        wheelPxPerZoomLevel: 70,
        wheelDebounceTime: 30
    });
    // 3000x3000 == rust map image size
    var bounds = [[0, 0], [3000, 3000]];
    // @ts-ignore
    var image = L.imageOverlay('static/images/map.jpg', bounds).addTo(leaflet_map);
    
    leaflet_map.fitBounds(bounds);

    leaflet_map_markers = L.featureGroup().addTo(leaflet_map);
    leaflet_monument_names = L.featureGroup().addTo(leaflet_map);
}

function drawMonuments(monumentData) {

}

/**
 * Receive a raw marker list in json format.
 * @param {any} markerData 
 */
export function receiveMarkers(markerData) {
    log(markerData);
    markerFactory.deleteAllMapMarkers();
    for (let i = 0; i < markerData.length; i++) {
        markers[i] = new Marker(markerData[i]);
        log(markers[i]);
        createMarker(markers[i]);
    }
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[map.js] ", "color: #E74C3C", ...args);
}
