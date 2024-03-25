//@ts-check
import * as socketio from "./socketio.js";
import { Marker, Monument } from "./structures.js";
import * as markerFactory from "./marker.js";
import { serverInfoInstance } from "./server.js";
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

// The size of the map image 
export const MAP_IMAGE_SZ = 2000;

export let map_sz = -9999;

/**
 * Get monument and first map marker data from server.
 * After this, map markers will be received every time
 * the server polls for them, they will arrive via socketio
 * broadcast at receiveMarkers()
 */
export async function initialiseMap() {
    map_sz = serverInfoInstance.map_size;
    log("Map size is", map_sz);
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
    let scale = MAP_IMAGE_SZ / map_sz;
    switch (marker.typeName) {
        case "PLAYER":
            markerFactory.createPlayerMarker(marker, scale);
            break;
        case "EXPLOSION":
            markerFactory.createExplosionMarker(marker, scale);
            break;
        case "SHOP":
            markerFactory.createShopMarker(marker, scale);
            break;
        case "CHINOOK":
            markerFactory.createChinookMarker(marker, scale);
            break;
        case "CARGOSHIP":
            markerFactory.createCargoMarker(marker, scale);
            break;
        case "CRATE":
            markerFactory.createCrateMarker(marker, scale);
            break;
        case "RADIUS":
            markerFactory.createRadiusMarker(marker, scale);
            break;
        case "ATTACKHELI":
            markerFactory.createHeliMarker(marker, scale);
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
        maxZoom: 2,
        zoomControl: false,
        zoomSnap: 0,
        wheelPxPerZoomLevel: 70,
        wheelDebounceTime: 30
    });
    
    var bounds = [[0, 0], [MAP_IMAGE_SZ, MAP_IMAGE_SZ]];
    // @ts-ignore
    var image = L.imageOverlay('static/images/map.jpg', bounds).addTo(leaflet_map);
    
    leaflet_map.fitBounds(bounds);
    leaflet_map.setZoom(-1.3);

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
    //log(markerData);
    markerFactory.deleteAllMapMarkers();
    for (let i = 0; i < markerData.length; i++) {
        markers[i] = new Marker(markerData[i]);
        //log(markers[i]);
        if (markers[i].typeName == "PLAYER") {
            createMarker(markers[i]);
            log("player at", markers[i].x, " ", markers[i].y);
        }
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
