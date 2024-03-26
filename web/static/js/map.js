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
 * @type {Map}
 */
export let plotted_markers = new Map();

export let leaflet_map;

export let map_markers;


export let leaflet_monument_names;

// The size of the map image 
export const MAP_IMAGE_SZ = 2000;

export let map_sz = -1;

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
    //@ts-ignore possibly null
    document.getElementById("map-container").style.backgroundColor = background_colour;

    // Request monument data from server
    const monumentData = (await socketio.request_topic("monuments")).monuments;
    log("MONUMENTS:", monumentData);


    const monuments = monumentData.map(data => new Monument(data));
    
    drawMonuments();

    // Request first set of map markers from server
    const markerData = (await socketio.request_topic("map_markers")).markers;
    receiveMarkers(markerData);
}

/**
 * Creates a leaflet marker object from the specified rust marker.
 * @param {Marker} marker - The marker object to plot on the map
 * @returns {L.Marker} A leaflet marker object
 */
function createMarker(marker) {
    let scale = MAP_IMAGE_SZ / map_sz;
    switch (marker.typeName) {
        case "PLAYER":
            return markerFactory.createPlayerMarker(marker, scale);
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

function initLeaflet() {
    // Initialize Leaflet map with a CRS
    // @ts-ignore
    leaflet_map = L.map('map-container', {
        // @ts-ignore
        crs: L.CRS.Simple,
        minZoom: -1.4,
        maxZoom: 2,
        zoomControl: false,
        zoomSnap: 0,
        wheelPxPerZoomLevel: 70,
        wheelDebounceTime: 30
    });
    
    var bounds = [[0, 0], [MAP_IMAGE_SZ, MAP_IMAGE_SZ]];

    L.imageOverlay('static/images/map.jpg', bounds).addTo(leaflet_map);
    
    leaflet_map.fitBounds(bounds);
    leaflet_map.setZoom(-1.1);

    map_markers = L.featureGroup().addTo(leaflet_map);

    leaflet_monument_names = L.featureGroup().addTo(leaflet_map);
}

function drawMonuments() {
    let scale = MAP_IMAGE_SZ / map_sz;
    // Create text for each monument
    for (let i = 0; i < monuments.length; i++) {
        let mon = monuments[i];
        /* Don't draw monuments that have no name
        (they weren't specified in the MonumentNames map) */
        if (!mon.name)
            continue;
        
        L.marker([mon.y * scale, mon.x * scale], {
            icon: L.divIcon({
                className: "monument-label",
                html: "<div style='text-align: center;'>" + mon.name + "</div>",
                iconSize: [100, 20],
                iconAnchor: [50, 10]
            })
        }).addTo(leaflet_monument_names);
    }
}

/**
 * Receive a raw marker list in json format.
 * @param {any} markerData - A JSON object containing map marker data
 */
export function receiveMarkers(markerData) {
    for (let i = 0; i < markerData.length; i++) {
        let marker = new Marker(markerData[i]);
        
        if (plotted_markers.get(marker.id))
            updateMarker(marker);
        else 
            plotted_markers.set(marker.id, createMarker(marker));
    }
}


function updateMarker(marker) {
    let scale = MAP_IMAGE_SZ / map_sz;
    var leaflet_marker = plotted_markers.get(marker.id);
    leaflet_marker.setLatLng(new L.latLng(marker.y * scale, marker.x * scale));
    leaflet_marker.setRotationAngle(360 - marker.rotation);
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[map.js] ", "color: #E74C3C", ...args);
}
