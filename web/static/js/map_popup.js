import { Marker } from "./structures.js";
import { nameFromSteamId } from "./steam.js";
import * as team from "./team.js";
import * as util from "./util.js";
import { plotted_markers } from "./map.js";
import { addShopToPopupDOM } from "./shopBrowser.js";

const DEBUG = true;

// Update popups every 5 seconds
const popupUpdateInterval = setInterval(updatePopups, 5000);

let bound_popups = [];

// Currently only used for shops and clustered shops
const popup_canvas = document.getElementById("map-popup-canvas");

function updatePopups() {
    log("Number of bound popups is", bound_popups.length);

    for (let i = 0; i < bound_popups.length; i++) {
        var leaflet_marker = bound_popups[i];
        var popup = leaflet_marker.getPopup();
        if (!popup)
            continue;
        // Don't update if it's open
        if (popup.isOpen())
            continue;

        // edge case for clustered shop
        if (leaflet_marker.is_clustered_shop) {
            popup.setContent(genClusteredShopPopupContent(leaflet_marker));
            continue;
        }

        switch (leaflet_marker.marker.typeName) {
            case "PLAYER":
                popup.setContent(genPlayerPopupContent(leaflet_marker)); break;
            case "EXPLOSION":
                popup.setContent(genExplosionPopupContent(leaflet_marker)); break;
            case "SHOP":
                popup.setContent(genShopPopupContent(leaflet_marker)); break;
            case "CHINOOK":
                popup.setContent(genChinookPopupContent(leaflet_marker)); break;
            case "CARGOSHIP":
                popup.setContent(genCargoPopupContent(leaflet_marker)); break;
            case "CRATE":
                popup.setContent(genCratePopupContent(leaflet_marker)); break;
            case "RADIUS":
                break;
            case "ATTACKHELI":
                popup.setContent(genHeliPopupContent(leaflet_marker)); break;
            default:
                log("Error: Unknown marker type in createMarker()");
        }
    }
    
}

export function hideMapPopup() {
    popup_canvas.style.display = "none";
}

export function bindMarkerPopup(leaflet_marker) {
    if (!leaflet_marker)
        return ;
    // edge case for clustered shop
    log(leaflet_marker.is_clustered_shop)
    if (leaflet_marker.is_clustered_shop) {
        leaflet_marker.bindPopup(genClusteredShopPopupContent(leaflet_marker), { className: "clustered-shop-map-popup" })
        bound_popups.push(leaflet_marker);
        return ;
    }

    if (!leaflet_marker.marker)
        return ;

    var marker = leaflet_marker.marker;
    switch (marker.typeName) {
        case "PLAYER":
            leaflet_marker.bindPopup(genPlayerPopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip(nameFromSteamId(marker.steam_id), { className: "leaflet-tooltip", direction: "top" });
            break;
        case "EXPLOSION":
            leaflet_marker.bindPopup(genExplosionPopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip("A debris field", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "SHOP":
            leaflet_marker.on("click", function() { addShopToPopupDOM(marker) });//bindPopup(genShopPopupContent(leaflet_marker), { className: "shop-map-popup" });
            leaflet_marker.bindTooltip("A Vending Machine", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "CHINOOK":
            leaflet_marker.bindPopup(genChinookPopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip("A Military Transport Helicopter", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "CARGOSHIP":
            leaflet_marker.bindPopup(genCargoPopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip("A Cargo Ship", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "CRATE":
            leaflet_marker.bindPopup(genCratePopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip("A Locked Crate", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "RADIUS":
            return //markerFactory.createRadiusMarker(marker, scale);
        case "ATTACKHELI":
            leaflet_marker.bindPopup(genHeliPopupContent(leaflet_marker), { className: "generic-map-popup" });
            leaflet_marker.bindTooltip("A Patrol Helicopter", { className: "leaflet-tooltip", direction: "top" });
            break;
        default:
            log("Error: Unknown marker type in createMarker()");
    }
    bound_popups.push(leaflet_marker);
}

// TODO: we can get rid of the update function if we pass marker_id
// To all of the popup generator functions
function makeShopPopup(marker_id) {
    if (!plotted_markers.has(marker_id)) {
        log("Tried to make a shop popup, but", marker_id, "isn't plotted?");
        return ;
    }

    // reset popup
    popup_canvas.innerHTML = "";

    // Get the latest leaflet marker for this shop
    var marker = plotted_markers.get(marker_id);

    
    



    log("HELLLOOOOOO", leaflet_marker);
}







function genPlayerPopupContent(leaflet_marker) {
    /** @type {Marker} */
    var player = leaflet_marker.marker;

    var player_name = nameFromSteamId(player.steam_id);
    var spawn_time = team.getSpawnTime(player.steam_id);
    var death_time = team.getDeathTime(player.steam_id);

    var spawned_at_time = "N/A"
    var died_at_time = "N/A";

    if (spawn_time > 0)
        spawned_at_time = util.formatTime(util.timeNow() - spawn_time);
    if (death_time > 0)
        died_at_time = util.formatTime(util.timeNow() - death_time);
    
    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>${player_name.toUpperCase()}</span>
    <div class='generic-popup-info-container'>
        <div class='generic-popup-info-table'>
            <table>
                <tr><th>SPAWNED</th><th>${spawned_at_time}</th><th>AGO</th></tr>
                <tr><th>DIED</th><th>${died_at_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}

function genShopPopupContent(leaflet_marker) {
    /** @type {Marker} */
    var shop = leaflet_marker.marker;


    var num_sale = shop.sell_orders;
    if (num_sale == 0)
        return "<h4>no items</h4>"

   // log(num_sale);

    return "<h3>" + shop.sell_orders[0].amount_in_stock + "</h3>";
}

function genCargoPopupContent(leaflet_marker) {
    /** @type {Marker} */

    var creation_time = "N/A";
    if (leaflet_marker.creation_time)
        creation_time = util.formatTime(util.timeNow() - leaflet_marker.creation_time);

    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>CARGOSHIP</span>
    
    <div class='generic-popup-info-container' style='height: 25px'>
        <div class='generic-popup-info-table' style='height: 25px'>
            <table>
                <tr><th>SPAWNED</th><th>${creation_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}

function genCratePopupContent(leaflet_marker) {
    /** @type {Marker} */

    var creation_time = "N/A";
    if (leaflet_marker.creation_time)
        creation_time = util.formatTime(util.timeNow() - leaflet_marker.creation_time);

    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>CRATE</span>
    
    <div class='generic-popup-info-container' style='height: 25px'>
        <div class='generic-popup-info-table' style='height: 25px'>
            <table>
                <tr><th>APPEARED</th><th>${creation_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}

function genExplosionPopupContent(leaflet_marker) {
    /** @type {Marker} */

    var creation_time = "N/A";
    if (leaflet_marker.creation_time)
        creation_time = util.formatTime(util.timeNow() - leaflet_marker.creation_time);

    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>EXPLOSION</span>
    
    <div class='generic-popup-info-container' style='height: 25px'>
        <div class='generic-popup-info-table' style='height: 25px'>
            <table>
                <tr><th>APPEARED</th><th>${creation_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}

function genHeliPopupContent(leaflet_marker) {
    /** @type {Marker} */

    var creation_time = "N/A";
    if (leaflet_marker.creation_time)
        creation_time = util.formatTime(util.timeNow() - leaflet_marker.creation_time);

    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>PATROL HELICOPTER</span>
    
    <div class='generic-popup-info-container' style='height: 25px'>
        <div class='generic-popup-info-table' style='height: 25px'>
            <table>
                <tr><th>SPAWNED</th><th>${creation_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}

function genChinookPopupContent(leaflet_marker) {
    /** @type {Marker} */

    var creation_time = "N/A";
    if (leaflet_marker.creation_time)
        creation_time = util.formatTime(util.timeNow() - leaflet_marker.creation_time);

    var popup = `
    <span style='margin-left:3px; padding-top:3px;'>CHINOOK</span>
    
    <div class='generic-popup-info-container' style='height: 25px'>
        <div class='generic-popup-info-table' style='height: 25px'>
            <table>
                <tr><th>SPAWNED</th><th>${creation_time}</th><th>AGO</th></tr>
            </table>
        </div>
    </div>
    `;

    return popup;
}


export function genClusteredShopPopupContent(clustered_shop_marker) {
    let shops_in_marker = clustered_shop_marker.shops;
    log(shops_in_marker)

    let content = `<b>This cluster represents ${shops_in_marker.length} shops.</b><br>`;
    shops_in_marker.forEach(shop => {
        var sell_orders = shop.sell_orders;
        sell_orders.forEach(sellOrder => {
            content += `<img src="static/images/items/${sellOrder.item_id}.png" width='50' height='50'/>`;
            content += `${shop.name} - ${sellOrder.currency_name} - ${sellOrder.item_name} - ${sellOrder.amount_in_stock}<br>`;
        });
        content += `<br><br>`;
    });
    return content;

}


/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[map_popup.js] ", "color: #7ebaec", ...args);
}
