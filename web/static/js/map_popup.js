import { Marker } from "./structures.js";
import { nameFromSteamId } from "./steam.js";
import * as team from "./team.js";
import * as util from "./util.js";

const DEBUG = true;

// Update popups every 5 seconds
const popupUpdateInterval = setInterval(updatePopups, 5000);

let bound_popups = [];

function updatePopups() {
    log("Number of bound popups is", bound_popups.length);

    for (let i = 0; i < bound_popups.length; i++) {
        var leaflet_marker = bound_popups[i];
        switch (leaflet_marker.marker.typeName) {
            case "PLAYER":
                leaflet_marker.getPopup().setContent(genPlayerPopupContent(leaflet_marker)); break;
            case "EXPLOSION":
                return //markerFactory.createExplosionMarker(marker, scale);
            case "SHOP":
                leaflet_marker.getPopup().setContent(genShopPopupContent(leaflet_marker)); break;
            case "CHINOOK":
                return //markerFactory.createChinookMarker(marker, scale);
            case "CARGOSHIP":
                return //markerFactory.createCargoMarker(marker, scale);
            case "CRATE":
                return //markerFactory.createCrateMarker(marker, scale);
            case "RADIUS":
                return //markerFactory.createRadiusMarker(marker, scale);
            case "ATTACKHELI":
                return //markerFactory.createHeliMarker(marker, scale);
            default:
                log("Error: Unknown marker type in createMarker()");
        }
    }
    
}

export function bindMarkerPopup(leaflet_marker) {
    if (!leaflet_marker || !leaflet_marker.marker)
        return ;
    var marker = leaflet_marker.marker;
    switch (marker.typeName) {
        case "PLAYER":
            leaflet_marker.bindPopup(genPlayerPopupContent(leaflet_marker), { className: "player-map-popup" });
            leaflet_marker.bindTooltip(nameFromSteamId(marker.steam_id), { className: "leaflet-tooltip", direction: "top" });
            break;
        case "EXPLOSION":
            return //markerFactory.createExplosionMarker(marker, scale);
        case "SHOP":
            leaflet_marker.bindPopup(genShopPopupContent(leaflet_marker), { className: "shop-map-popup" });
            leaflet_marker.bindTooltip("A Vending Machine", { className: "leaflet-tooltip", direction: "top" });
            break;
        case "CHINOOK":
            return //markerFactory.createChinookMarker(marker, scale);
        case "CARGOSHIP":
            return //markerFactory.createCargoMarker(marker, scale);
        case "CRATE":
            return //markerFactory.createCrateMarker(marker, scale);
        case "RADIUS":
            return //markerFactory.createRadiusMarker(marker, scale);
        case "ATTACKHELI":
            return //markerFactory.createHeliMarker(marker, scale);
        default:
            log("Error: Unknown marker type in createMarker()");
    }
    bound_popups.push(leaflet_marker);
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
    
    var is_online = player.is_online ? "online" : "offline";

    var popup = `
    <span style='margin-left:5px; padding-top:3px;'>${player_name.toUpperCase()}
        <span style='float:right; padding-right: 5px;'>
            <div class='${is_online}-circle'></div>
        </span>
    </span>
    <div class='player-popup-info-container'>
        <div class='player-popup-info-table'>
            <table>
                <tr><th>SPAWN TIME</th><th>${spawned_at_time}</th></tr>
                <tr><th>DEATH TIME</th><th>${died_at_time}</th></tr>
            </table>
        </div>
    </div>
    `;
    //<img width='15px' height='15px' src='static/images/rust/${is_online}.png'/>
    //var popup = "<h3>" + team.getName(player.steam_id) + "</h3>" + "<p>" + spawn_time + "</p>";

    return popup;
}

function genShopPopupContent(leaflet_marker) {
    /** @type {Marker} */
    var shop = leaflet_marker.marker;


    var num_sale = shop.sell_orders;

   // log(num_sale);

    return "<h3>" + shop.sell_orders[0].cost_per_item + "</h3>";
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[map_popup.js] ", "color: #7ebaec", ...args);
}
