//@ts-check

import { Marker, SellOrder } from "./structures.js";


const DEBUG = true;

/*
    <div class="popup-shop-container">
        <div class="popup-shop-header">
            <div class="popup-shop-header-title">
                Tools & Stuff
            </div>
            <div class="popup-shop-header-image-row">
                <div class="popup-shop-header-image-cell"></div>
                <div class="popup-shop-header-image-cell"></div>
                <div class="popup-shop-header-image-cell"></div>
                <div class="popup-shop-header-image-cell"></div>
            </div>
            <div id="chevron1" class="popup-shop-header-chevron popup-shop-header-chevron-down"></div>
            </div>


        let note = document.createElement("div");
	note.className = "overlay map_note " + (web_note ? "web_map_note" : "");

	if (web_note)
		note.id = "overlay_web_note" + id;
	else
		note.id = "overlay_note" + id;

	note.style.fontSize = "10px";
	note.innerHTML = label;
	//note.style.backgroundImage = `url('${img_path}/markers/bed.png')`;

	
    if (icon_index == 0) {
        note.style.mask = `url('${img_path}/markers/${icon_index}.png') no-repeat center / contain`; // icon
        note.style.backgroundColor = `${colour}`; // icon colour
    } else {

        let note_backg = document.createElement("div");
        note_backg.className = "note-background";
        note_backg.style.backgroundColor = darkenRGB(colour);//"#40411a"; // background colour
        //background-color: #f0f0f0;


        let note_mask = document.createElement("div");
        note_mask.className = "note-mask";
        note_mask.style.mask = `url('${img_path}/markers/${icon_index}.png') no-repeat center / contain`; // icon
        note_mask.style.maskSize = "60%";
        note_mask.style.backgroundColor = `${colour}`; // icon colour

*/

function createDiv() {
    return document.createElement("div");
}

/**
 * 
 * @param {Marker[]} shops 
 */
export function addClusterShopPopupDOM(shops) {
    var container = document.getElementById("map-popup-content-canvas");
    container.innerHTML = "";
    for (let i = 0; i < shops.length; i++) {
        container.appendChild(createShopPopupContainer(shops[i]));
        makeShopBodyToggleable(shops[i].id);
    }
    document.getElementById("map-popup").style.visibility = "visible";
}

/**
 * 
 * @param {Marker} shop 
 */
export function addShopToPopupDOM(shop) {
    var container = document.getElementById("map-popup-content-canvas");
    container.innerHTML = "";
    
    container.appendChild(createShopPopupContainer(shop));
    
    makeShopBodyToggleable(shop.id);
    document.getElementById("map-popup").style.visibility = "visible";
}



/**
 * 
 * @param {Marker} shop 
 */
function createShopPopupContainer(shop) {
    let popup_shop_container = createDiv();
    popup_shop_container.classList.add("popup-shop-container");
    popup_shop_container.appendChild(createPopupShopHeader(shop));
    popup_shop_container.appendChild(createPopupShopBody(shop));
    return popup_shop_container;
}
/**
 * 
 * @param {Marker} shop 
 */
function createPopupShopHeader(shop) {
    let popup_shop_header = createDiv();
    popup_shop_header.classList.add("popup-shop-header");
    
    let popup_shop_header_title = createDiv();
    popup_shop_header_title.classList.add("popup-shop-header-title");
    popup_shop_header_title.innerHTML = shop.name;
    popup_shop_header.appendChild(popup_shop_header_title);

    let popup_shop_header_image_row = createDiv();
    popup_shop_header_image_row.classList.add("popup-shop-header-image-row");
    for (let i = 0; i < 4; i++) {
        let popup_shop_header_image_cell = createDiv();
        popup_shop_header_image_cell.classList.add("popup-shop-header-image-cell");
        if (shop.sell_orders[i] && shop.sell_orders[i].item_id)
            popup_shop_header_image_cell.style.backgroundImage = `url("static/images/items/${shop.sell_orders[i].item_id}.png")`;
        popup_shop_header_image_row.appendChild(popup_shop_header_image_cell);
    }
    popup_shop_header.appendChild(popup_shop_header_image_row);

    let popup_shop_header_chevron = createDiv();
    popup_shop_header_chevron.id = "chevron" + shop.id;
    popup_shop_header_chevron.classList.add("popup-shop-header-chevron");
    popup_shop_header_chevron.classList.add("popup-shop-header-chevron-down");
    popup_shop_header.appendChild(popup_shop_header_chevron);

    return popup_shop_header;
}

/**
 * 
 * @param {Marker} shop 
 */
function createPopupShopBody(shop) {
    let popup_shop_body = createDiv();
    popup_shop_body.id = "shop-body" + shop.id;
    popup_shop_body.classList.add("popup-shop-body");
    
    let shop_body_items = createDiv();
    shop_body_items.classList.add("shop-body-items");

    for (let i = 0; i < shop.sell_orders.length; i++)
        // @ts-ignore
        shop_body_items.appendChild(createShopBodyItem(shop.sell_orders[i]));

    popup_shop_body.appendChild(shop_body_items);

    return popup_shop_body;
}

/**
 * 
 * @param {SellOrder} sell_order 
 */
function createShopBodyItem(sell_order) {
    let shop_body_item = createDiv();
    shop_body_item.classList.add("shop-body-item");

    let shop_body_item_cell1 = createDiv();
    shop_body_item_cell1.classList.add("shop-body-item-cell");

    let shop_body_item_image = createDiv();
    shop_body_item_image.classList.add("shop-body-item-image");
    shop_body_item_image.style.backgroundImage = `url("static/images/items/${sell_order.item_id}.png")`;
    shop_body_item_cell1.appendChild(shop_body_item_image);

    let shop_body_item_selling_info = createDiv();
    shop_body_item_selling_info.classList.add("shop-body-item-selling-info");
    let shop_body_item_selling_title = createDiv();
    shop_body_item_selling_title.classList.add("shop-body-item-selling-title");
    shop_body_item_selling_title.innerHTML = "SELLING";
    let shop_body_item_selling_amount = createDiv();
    shop_body_item_selling_amount.classList.add("shop-body-item-selling-amount");
    shop_body_item_selling_amount.innerHTML = sell_order.cost_per_item;
    shop_body_item_selling_info.appendChild(shop_body_item_selling_title);
    shop_body_item_selling_info.appendChild(shop_body_item_selling_amount);
    shop_body_item_cell1.appendChild(shop_body_item_selling_info);

    shop_body_item.appendChild(shop_body_item_cell1);
    
    let shop_body_item_cell2 = createDiv();
    shop_body_item_cell2.classList.add("shop-body-item-cell");

    let shop_body_cost_image = createDiv();
    shop_body_cost_image.classList.add("shop-body-cost-image");
    shop_body_cost_image.style.backgroundImage = `url("static/images/items/${sell_order.currency_id}.png")`;
    shop_body_item_cell2.appendChild(shop_body_cost_image);

    let shop_body_cost_info = createDiv();
    shop_body_cost_info.classList.add("shop-body-cost-info");
    let shop_body_item_cost_title = createDiv();
    shop_body_item_cost_title.classList.add("shop-body-item-selling-title");
    shop_body_item_cost_title.innerHTML = "COST";
    let shop_body_item_cost_amount = createDiv();
    shop_body_item_cost_amount.classList.add("shop-body-item-selling-amount");
    shop_body_item_cost_amount.innerHTML = sell_order.cost_per_item;
    shop_body_cost_info.appendChild(shop_body_item_cost_title);
    shop_body_cost_info.appendChild(shop_body_item_cost_amount);
    shop_body_item_cell2.appendChild(shop_body_cost_info);

    shop_body_item.appendChild(shop_body_item_cell2);

    let shop_body_item_cell3 = createDiv();
    shop_body_item_cell3.classList.add("shop-body-item-cell");

    let shop_body_in_stock = createDiv();
    shop_body_in_stock.classList.add("shop-body-in-stock");
    shop_body_in_stock.innerHTML = sell_order.amount_in_stock + " IN STOCK";
    shop_body_item_cell3.appendChild(shop_body_in_stock);

    shop_body_item.appendChild(shop_body_item_cell3);

    return shop_body_item;
}

function makeShopBodyToggleable(shop_id) {
    var chevron = document.getElementById("chevron" + shop_id);
    // @ts-ignore
    chevron.addEventListener('click', function() {
        var content = document.getElementById("shop-body" + shop_id);        
        if (this.classList.contains('popup-shop-header-chevron-down')) {
            // Expand the content
            // @ts-ignore
            content.style.maxHeight = content.scrollHeight + "px";
            this.classList.remove('popup-shop-header-chevron-down');
            this.classList.add('popup-shop-header-chevron-up');
        } else {
            // Collapse the content
            // @ts-ignore
            content.style.maxHeight = 0 + "px";
            this.classList.remove('popup-shop-header-chevron-up');
            this.classList.add('popup-shop-header-chevron-down');
        }
    });
}

/*

      <div class="shop-body-item">


        <div class="shop-body-item-cell">
          <div class="shop-body-cost-image"></div>
          <div class="shop-body-cost-info">
            <div class="shop-body-item-selling-title"> COST </div>
            <div class="shop-body-item-selling-amount"> 40 </div>
          </div>
        </div>
        <div class="shop-body-item-cell">
          <div class="shop-body-in-stock">10 IN STOCK</div>
        </div>
      </div>
    </div>


  </div>



</div>
*/


/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[shopBrowser.js] ", "color: #a5e82f", ...args);
}