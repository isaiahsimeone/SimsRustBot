//@ts-check

import { Marker, SellOrder } from "./structures.js";
import { countEmojiCharacters, emojifyText } from "./emoji.js";

const DEBUG = true;

/**
 * Creates a div (without adding it to the DOM) with a class name
 * and id, both optional.
 * @param {string} class_name A class to be added to the div
 * @param {string} element_id The ID this div should have
 * @returns The created div
 */
function createDiv(class_name="", element_id="") {
    var div = document.createElement("div");
    if (class_name != "")
        div.classList.add(class_name);
    if (element_id != "")
        div.id = element_id;
    return div;
}

/**
 * Gets the specified element from the DOM
 * @param {string} element_id the element to get a reference to
 * @returns The target document, or a body tag in error
 */
function DOMSafeGetById(element_id) {
    var target = document.getElementById(element_id);
    if (!target) {
        log("ERROR: Could not find element with id:", element_id);
        // Return this to suppress typescript errors, if
        // it's added to the dom, we'll know, because
        // shit will break
        return document.createElement("body");
    }
    return target;
}

/**
 * A list of shops to create a clustered shop popup from.
 * @param {Marker[]} shops - The shops to add to the shop popup
 */
export function addClusterShopPopupDOM(shops) {
    var container = DOMSafeGetById("map-popup-content-canvas");
    container.innerHTML = "";
    for (let i = 0; i < shops.length; i++) {
        container.appendChild(createShopPopupContainer(shops[i]));
        makeShopBodyToggleable(shops[i].id);
    }
    DOMSafeGetById("map-popup").style.visibility = "visible";
}

/**
 * Add the specified SINGLE shop to the shop browser popup
 * @param {Marker} shop The shop marker to create a popup for
 */
export function addShopToPopupDOM(shop) {
    var container = DOMSafeGetById("map-popup-content-canvas");

    container.innerHTML = "";
    
    container.appendChild(createShopPopupContainer(shop));
    
    // start expanded for single shop
    expandShopBody(shop.id);
    makeShopBodyToggleable(shop.id);

    var map_popup_pane = DOMSafeGetById("map-popup");

    map_popup_pane.style.visibility = "visible";
}

/**
 * Create a popup shop container from the specified shop marker
 * The marker is expected to be a shop
 * @param {Marker} shop - The marker to create a popup-shop-container from
 */
function createShopPopupContainer(shop) {
    let popup_shop_container = createDiv("popup-shop-container");
    popup_shop_container.appendChild(createPopupShopHeader(shop));
    popup_shop_container.appendChild(createPopupShopBody(shop));
    return popup_shop_container;
}

/**
 * Create a header (uncollapsed entry in shop browser). for a shop
 * returns a div of class popup-shop-header to be added to the popup-shop-container
 * @param {Marker} shop - The marker of the shop header to create a header for
 */
function createPopupShopHeader(shop) {
    let popup_shop_header = createDiv("popup-shop-header");
    
    let popup_shop_header_title = createDiv("popup-shop-header-title");
    
    if (shop.name.length - countEmojiCharacters(shop.name) > 18) {
        let popup_shop_header_title_scroll = createDiv("popup-shop-header-title-scroll");
        popup_shop_header_title_scroll.innerHTML = emojifyText(shop.name);
        popup_shop_header_title.appendChild(popup_shop_header_title_scroll);
    } else
        popup_shop_header_title.innerHTML = emojifyText(shop.name);

    popup_shop_header.appendChild(popup_shop_header_title);

    let popup_shop_header_image_row = createDiv("popup-shop-header-image-row");
    for (let i = 0; i < 4; i++) {
        let popup_shop_header_image_cell = createDiv("popup-shop-header-image-cell");
        if (shop.sell_orders[i] && shop.sell_orders[i].item_id)
            popup_shop_header_image_cell.style.backgroundImage = `url("static/images/items/${shop.sell_orders[i].item_id}.png")`;
        popup_shop_header_image_row.appendChild(popup_shop_header_image_cell);
    }
    popup_shop_header.appendChild(popup_shop_header_image_row);

    let popup_shop_header_chevron = createDiv("popup-shop-header-chevron", "chevron" + shop.id);
    popup_shop_header_chevron.classList.add("popup-shop-header-chevron-down");
    popup_shop_header.appendChild(popup_shop_header_chevron);

    return popup_shop_header;
}

/**
 * Create a popup-shop-body class div to be added to a div of class popup-shop-container.
 * Each sell order in the shop will create a separate entry in the shop browser
 * @note these are hidden by default in other parts of the program see hideMapPopup()
 * @param {Marker} shop The Marker of the shop to create the popup shop body for
 */
function createPopupShopBody(shop) {
    let popup_shop_body = createDiv("popup-shop-body", "shop-body" + shop.id);
    let shop_body_items = createDiv("shop-body-items");

    if (shop.sell_orders.length == 0)
        shop_body_items.appendChild(createShopBodyNoListings());
    else
        for (let i = 0; i < shop.sell_orders.length; i++)
            shop_body_items.appendChild(createShopBodyItem(shop.sell_orders[i]));
    
    popup_shop_body.appendChild(shop_body_items);
    return popup_shop_body;
}

function createShopBodyNoListings() {
    let shop_body_item = createDiv("shop-body-item");
    let shop_body_item_cell1 = createDiv("shop-body-item-cell");
    let shop_body_item_no_listing_text = createDiv("shop-body-item-no-listing-text");
    shop_body_item_no_listing_text.innerHTML = "This vendor has no listings.";
    shop_body_item_cell1.appendChild(shop_body_item_no_listing_text);
    shop_body_item.appendChild(shop_body_item_cell1);
    
    return shop_body_item;
}

/**
 * Create a Shop Body div to be appended to a shop-body-items
 * class. It represents a row in a shop entry in the shop browser popup
 * @param {SellOrder} sell_order The sell order of the shop entry. It has the
 *                               item for sale, the currency of the item, etc
 */
function createShopBodyItem(sell_order) {
    let shop_body_item = createDiv("shop-body-item");

    let shop_body_item_cell1 = createDiv("shop-body-item-cell");

    let shop_body_item_image = createDiv("shop-body-item-image");
    shop_body_item_image.style.backgroundImage = `url("static/images/items/${sell_order.item_id}.png")`;
    let tooltip = document.createElement("span");
    tooltip.classList.add("rust-image-tooltip");
    tooltip.innerHTML = sell_order.item_name;
    shop_body_item_image.appendChild(tooltip);
    shop_body_item_cell1.appendChild(shop_body_item_image);

    let shop_body_item_selling_info = createDiv("shop-body-item-selling-info");
    let shop_body_item_selling_title = createDiv("shop-body-item-selling-title");
    shop_body_item_selling_title.innerHTML = "SELLING";
    let shop_body_item_selling_amount = createDiv("shop-body-item-selling-amount");
    shop_body_item_selling_amount.innerHTML = sell_order.cost_per_item;
    shop_body_item_selling_info.appendChild(shop_body_item_selling_title);
    shop_body_item_selling_info.appendChild(shop_body_item_selling_amount);
    shop_body_item_cell1.appendChild(shop_body_item_selling_info);

    let shop_body_item_cell2 = createDiv("shop-body-item-cell");

    let shop_body_cost_image = createDiv("shop-body-cost-image");
    shop_body_cost_image.style.backgroundImage = `url("static/images/items/${sell_order.currency_id}.png")`;
    let tooltip1 = document.createElement("span");
    tooltip1.classList.add("rust-image-tooltip");
    tooltip1.innerHTML = sell_order.currency_name;
    shop_body_cost_image.appendChild(tooltip1);
    shop_body_item_cell2.appendChild(shop_body_cost_image);

    let shop_body_cost_info = createDiv("shop-body-cost-info");
    let shop_body_item_cost_title = createDiv("shop-body-item-selling-title");
    shop_body_item_cost_title.innerHTML = "COST";
    let shop_body_item_cost_amount = createDiv("shop-body-item-selling-amount");
    shop_body_item_cost_amount.innerHTML = sell_order.cost_per_item;
    shop_body_cost_info.appendChild(shop_body_item_cost_title);
    shop_body_cost_info.appendChild(shop_body_item_cost_amount);
    shop_body_item_cell2.appendChild(shop_body_cost_info);

    let shop_body_item_cell3 = createDiv("shop-body-item-cell");

    let shop_body_in_stock = createDiv();
    if (sell_order.amount_in_stock > 0) {
        shop_body_in_stock.classList.add("shop-body-in-stock");
        shop_body_in_stock.innerHTML = sell_order.amount_in_stock + " IN STOCK";
    } else {
        shop_body_in_stock.classList.add("shop-body-no-stock");
        shop_body_in_stock.innerHTML = "SOLD OUT";
    }
    
    shop_body_item_cell3.appendChild(shop_body_in_stock);
    
    if (sell_order.amount_in_stock <= 0) {
        shop_body_item.style.backgroundColor = "rgb(68, 40, 32)";
        shop_body_item_cell1.style.backgroundColor = "rgb(68, 40, 32)";
        shop_body_item_cell2.style.backgroundColor = "rgb(68, 40, 32)";
        shop_body_item_cell3.style.backgroundColor = "rgb(68, 40, 32)";
    }
    
    shop_body_item.appendChild(shop_body_item_cell1);
    shop_body_item.appendChild(shop_body_item_cell2);
    shop_body_item.appendChild(shop_body_item_cell3);

    return shop_body_item;
}

/**
 * Make the shop popup body with the specified id expandable and
 * collapsable
 * @param {number} shop_id The ID of the shop to make toggleable
 */
function makeShopBodyToggleable(shop_id) {
    var chevron = DOMSafeGetById("chevron" + shop_id);

    chevron.addEventListener('click', function() {
        if (this.classList.contains('popup-shop-header-chevron-down'))
            expandShopBody(shop_id);
        else 
            collapseShopBody(shop_id);
    });
}

/**
 * Collapse the shop body of the popup shop with the specified ID
 * @param {number} shop_id The ID of the shop to make collapsable
 */
function collapseShopBody(shop_id) {
    var shop_body = DOMSafeGetById("shop-body" + shop_id);

    // Restrict shop body height property
    shop_body.style.maxHeight = 0 + "px";

    // Flip the chevron to down
    var chevron = DOMSafeGetById("chevron" + shop_id);

    if (chevron.classList.contains("popup-shop-header-chevron-up"))
        chevron.classList.remove("popup-shop-header-chevron-up");
    // Flip the chevron up
    chevron.classList.add('popup-shop-header-chevron-down');
}

/**
 * Expand the shop body of the popup shop with the specified ID
 * @param {number} shop_id The ID of the shop to expand
 */
function expandShopBody(shop_id) {
    var shop_body = DOMSafeGetById("shop-body" + shop_id);

    // Allow shop body height property to be > 0
    shop_body.style.maxHeight = shop_body.scrollHeight + "px";

    // Flip the chevron to up
    var chevron = DOMSafeGetById("chevron" + shop_id);
    if (chevron.classList.contains("popup-shop-header-chevron-down"))
        chevron.classList.remove("popup-shop-header-chevron-down");
    // Flip the chevron up
    chevron.classList.add('popup-shop-header-chevron-up');
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[shopBrowser.js] ", "color: #a5e82f", ...args);
}