//@ts-check
import * as socketio from "./socketio.js";
import { Marker, Monument } from "./structures.js";
import * as markerFactory from "./marker.js";
import { serverInfoInstance } from "./server.js";
import { steamImageExists } from "./steam.js";
import { bindMarkerPopup, hideMapPopup } from "./map_popup.js";
import { showMapNoteDialog } from "./map_notes.js";
//import { receiveMapNotes } from "./note.js";
//import { receiveTeamMembers } from "./steam.js";
//import { toggleChatAvailability } from "./chat.js";

const DEBUG = true;
const CLUSTER_DISABLE_THRESHOLD = 300;
export const MAP_IMAGE_SZ = 2000;
export let CLUSTERING_THRESHOLD = 13;

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

export let leaflet_shop_markers;

export let all_shops = new Map();

export let leaflet_monument_names;

export let leaflet_map_note_dialog;

export let leaflet_custom_map_notes;

// The size of the map image 

export let map_sz = -1;

let initial_clustering_complete = false;

let clustered_shop_markers = [];

let shop_marker_id_to_cluster_id = new Map();

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

    // Add listener for a click on the map, which should close popups
    document.getElementById("map-container")?.addEventListener("click", function(event) {
        // Check if the clicked element is the map container itself and not a child
        if (event.target === document.getElementById("map-container")) {
            hideMapPopup();
        }
    });

    // Hook context click for map note creation
    leaflet_map.on("contextmenu",(e) => {
        showMapNoteDialog(e);
        /**/
      });

    // Request background colour from server
    background_colour = (await socketio.request_topic("background")).background;
    log("background colour is", background_colour);
    //@ts-ignore possibly null
    document.getElementById("map-container").style.backgroundColor = background_colour;

    // Request monument data from server
    const monumentData = (await socketio.request_topic("monuments")).monuments;
    log("MONUMENTS:", monumentData);
    monuments = monumentData.map(data => new Monument(data));
    drawMonuments();

    // Request first set of map markers from server
    const markerData = (await socketio.request_topic("map_markers")).markers;
    receiveMarkers(markerData);
    
    // Get the time that heli's/cargo's first appeared on the map
    const eventStartTimes = (await socketio.request_topic("event_start_times")).start_times;
    Object.keys(eventStartTimes).forEach(key => {
        setCreationTime(key, eventStartTimes[key]);
    });

    // Cluster shops - If there isn't a hectic number of shops
    if (all_shops.size < CLUSTER_DISABLE_THRESHOLD) {
        var startTime = performance.now();
        log(all_shops.size);
        clusterCloseShops(all_shops);
        log(all_shops.size);
        var endTime = performance.now();
        log(`Shop clustering took ${endTime - startTime} ms`);
    }
    initial_clustering_complete = true;
}

/**
 * Creates a leaflet marker object from the specified rust marker.
 * @param {Marker} marker - The marker object to plot on the map
 * @returns {L.Marker} A leaflet marker object
 */
function createMarker(marker) {
    let scale = MAP_IMAGE_SZ / map_sz;
    var m;
    switch (marker.typeName) {
        case "PLAYER":
            m = markerFactory.createPlayerMarker(marker, scale); break;
        case "EXPLOSION":
            m = markerFactory.createExplosionMarker(marker, scale); break;
        case "SHOP":
            m = markerFactory.createShopMarker(marker, scale); break;
        case "CHINOOK":
            m = markerFactory.createChinookMarker(marker, scale); break;
        case "CARGOSHIP":
            m = markerFactory.createCargoMarker(marker, scale); break;
        case "CRATE":
            m = markerFactory.createCrateMarker(marker, scale); break;
        case "RADIUS":
            m = markerFactory.createRadiusMarker(marker, scale); break;
        case "ATTACKHELI":
            m = markerFactory.createHeliMarker(marker, scale); break;
        default:
            log("Error: Unknown marker type in createMarker()");
    }
    bindMarkerPopup(m);
    return m;
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
    leaflet_shop_markers = L.featureGroup().addTo(leaflet_map);
    leaflet_monument_names = L.featureGroup().addTo(leaflet_map);
    leaflet_map_note_dialog = L.featureGroup().addTo(leaflet_map);
    leaflet_custom_map_notes = L.featureGroup().addTo(leaflet_map);
}

function drawMonuments() {
    log("monuments are:", monuments);
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
            }),
            zIndexOffset: -10 // Appear behind map icons
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

        // If this shop exists, it could be in a cluster, update its content
        if (marker.typeName == "SHOP") {
            updateClusterResident(marker);
        }

        if (plotted_markers.has(marker.id)) {
            updateMarker(marker);
            continue;
        } 
        // New marker
        var created_marker = createMarker(marker);
        // Recalc clusters if it's a new shop
        if (marker.typeName == "SHOP" && !all_shops.has(marker.id)) {
            all_shops.set(marker.id, created_marker);
            // New shop marker added (after initialiseMap). Recluster
            if (initial_clustering_complete && all_shops.size < CLUSTER_DISABLE_THRESHOLD) {
                log("X");
                clusterCloseShops(all_shops);
            }
            
        } 


        plotted_markers.set(marker.id, created_marker);
    }
}

/**
 * Remove a marker from the leaflet map with the provided id.
 * (rust marker ID)
 * @param {string} marker_id 
 */
export function removeMarker(marker_id) {
    
    log("removing marker: ", marker_id);

    if (!plotted_markers)
        return ;

    var target_marker = plotted_markers.get(marker_id);
    if (!target_marker)
        return ;

    leaflet_map.removeLayer(target_marker);
    plotted_markers.delete(marker_id);
}

export function setCreationTime(marker_id, creation_time) {
    if (!plotted_markers)
        return ;
    var target_marker = plotted_markers.get(marker_id);
    if (!target_marker)
        return ;
    
    target_marker.creation_time = creation_time;
    log(target_marker);
    plotted_markers.set(marker_id, target_marker);
}

function updateMarker(marker) {
    let scale = MAP_IMAGE_SZ / map_sz;
    var leaflet_marker = plotted_markers.get(marker.id);
    if (!leaflet_marker || !leaflet_marker.marker)
        return ;
    var stored_marker = leaflet_marker.marker;

    if (stored_marker.id != marker.id) {
        log("ERROR: Marker Id doesn't match the stored marker id");
        return ;
    }

    // Load a steam image for player markers
    if (marker.typeName == "PLAYER" && !leaflet_marker.image_loaded) {
        if (!steamImageExists(marker.steam_id))
            return ;

        leaflet_marker.remove();
        // createMarker will load the steam image
        plotted_markers.set(marker.id, createMarker(marker));
    }

    leaflet_marker.setLatLng(new L.latLng(marker.y * scale, marker.x * scale));
    leaflet_marker.setRotationAngle(360 - marker.rotation);
    leaflet_marker.marker = marker;
}














/**
 * Organise a list of shops into clusters on the map, within a distance
 * threshold (cluster_threshold)
 * @param {L.Marker} shop_markers - A list of leaflet markers that are rust shops 
 */
function clusterCloseShops(shop_markers) {
    // TODO: Brute force clustering is horrific
    let clusters = [];
    let clusteredMarkers = new Set();

    const markersArray = Array.from(shop_markers.values());

    // O(n^2) - could preprocess with bucketing to probably get O(n) 
    markersArray.forEach(marker => {
        // Skip if this marker is already clustered
        if (clusteredMarkers.has(marker)) 
            return ; 
        
        let cluster = [marker];
        markersArray.forEach(otherMarker => {
            if (marker !== otherMarker && !clusteredMarkers.has(otherMarker)) {
                
                let distance = calculateDistance(marker, otherMarker);
                if (distance <= CLUSTERING_THRESHOLD) {
                    cluster.push(otherMarker);
                    // This marker is part of a cluster
                    clusteredMarkers.add(otherMarker); 
                }
            }
        });

        // Only consider it a cluster if more than one marker is close together
        if (cluster.length > 1) {
            clusters.push(cluster);
        }
    });
    log("clusters", clusters);
    // Update the map with the clusters
    updateMapWithClusters(clusters, clusteredMarkers, shop_markers);
}

function updateMapWithClusters(clusters, clusteredMarkers, shop_markers) {
    // Step 1: Hide all markers initially
    shop_markers.forEach((value, key) => {
        leaflet_map.removeLayer(value); // Ensure value, which is the marker, is used
    });
    // Step 1.1: Remove all current clusters on the map
    clustered_shop_markers.forEach(shop_marker => {
        leaflet_map.removeLayer(shop_marker);
    });

    let nonClusteredMarkers = new Set(); // To track non-clustered markers
    let cluster_index = 0;
    // Step 2: Process clusters and show cluster markers
    clusters.forEach(cluster => {
        let centroid = { lat: 0, lng: 0 };
        var shops_in_cluster = [];
        cluster.forEach(marker => {
            centroid.lat += marker.getLatLng().lat;
            centroid.lng += marker.getLatLng().lng;
            // Add the shop this marker denotes to the cluster
            shops_in_cluster.push(marker.marker);
            // Mark this marker as processed
            clusteredMarkers.add(marker);
        });

        centroid.lat /= cluster.length;
        centroid.lng /= cluster.length;

        // Add cluster marker for this cluster
        //var popup_content = `This cluster represents ${cluster.length} shops.`;
        
        var clustered_shop = L.marker([centroid.lat, centroid.lng], {
            icon: L.divIcon({
                html: `<div style="z-index: -9;position: relative; text-align: center; width: 20px; height: 20px;">
                         <img src="static/images/rust/cluster_shop.png" style="width: 100%; height: 100%;">
                         <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.8); color: white;"><b>${cluster.length}</b></span>
                       </div>`,
                className: '',
                zIndexOffset: -9, // TODO: why does this not do anything
                iconSize: [20, 20] // Adjust size as needed
            })
        }).addTo(leaflet_map).bindTooltip("Multiple Vending Machines", { className: "leaflet-tooltip", direction: "top" });
        
        // The shops in this cluster will need to be updated. Maintain a map of the shop marker ID
        // To this cluster, so we can look up the shop ID, and determine the cluster it is in
        for (let i = 0; i < shops_in_cluster.length; i++) {
            shop_marker_id_to_cluster_id.set(shops_in_cluster[i].id, cluster_index);
        }

        clustered_shop.shops = shops_in_cluster;
        
        clustered_shop.is_clustered_shop = true;
        bindMarkerPopup(clustered_shop);

        clustered_shop_markers.push(clustered_shop);

        cluster_index++;
    });

    // Determine non-clustered markers by excluding clustered markers from all markers
    shop_markers.forEach((marker, key) => {
        if (!clusteredMarkers.has(marker)) {
            nonClusteredMarkers.add(marker);
        }
    });

    // Step 3 & 4: Re-add non-clustered markers to the map
    nonClusteredMarkers.forEach(marker => {
        marker.addTo(leaflet_map); // Now correctly adding only Leaflet markers
    });
}

/**
 * 
 * @param {Marker} new_marker 
 */
function updateClusterResident(new_marker) {
    
    // What cluster is this shop in?
    if (!shop_marker_id_to_cluster_id.has(new_marker.id))
        return ; // Not in a cluster
    // The ID of the cluster this shop is in
    let cluster_id = shop_marker_id_to_cluster_id.get(new_marker.id);
    // Shops (Rust markers) in this cluster
    let shops = clustered_shop_markers[cluster_id].shops;
    
    // Iterate through each shop in the cluster, update the target resident
    for (let i = 0; i < shops.length; i++) {
        // Found the target, update the list directly
        if (shops[i].id == new_marker.id) {
            clustered_shop_markers[cluster_id].shops[i] = new_marker;
            break;
        }
    }
}


function calculateDistance(markerA, markerB) {
    const latLngA = markerA.getLatLng();
    const latLngB = markerB.getLatLng();

    const dx = latLngA.lng - latLngB.lng;
    const dy = latLngA.lat - latLngB.lat;

    return Math.sqrt(dx * dx + dy * dy);
}




/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[map.js] ", "color: #E74C3C", ...args);
}
