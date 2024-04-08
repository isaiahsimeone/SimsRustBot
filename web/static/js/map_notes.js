import { my_steam_id, nameFromSteamId } from "./steam.js";
import * as socketio from "./socketio.js";
import { leaflet_map_note_dialog, leaflet_custom_map_notes } from "./map.js";
import { darkenRGB, rgb2hex, createDiv, safeGetId, safeGetClassName } from "./util.js";
import { img_path } from "./main.js";

const DEBUG = true;

//TODO: vars here to record selected colour and other stuff when resummoning the popup box

export function initialiseMapNotes() {

}

let dialog_open = false;

let selected_note_icon_index = 0;
let selected_note_colour_index = 0;
let selected_note_icon_colour = "#cbcd53";
let popup_open_location = null;

/**
 * A leaflet marker used to show where the marker will be placed
 * when apply is clicked
 */
let temp_marker = null;
let temp_marker_icon = null;


export function showMapNoteDialog(event) {
    if (dialog_open)
        return ;
    dialog_open = true;
    // Destroy map note dialog if it's active
	popup_open_location = event.latlng;
    log(selected_note_colour_index, selected_note_icon_index);
	// Get the dialog element and position it at the click location
	var dialog = safeGetId("map-note-dialog", log);
    log(dialog);

    var popup_document = new DOMParser().parseFromString(dialog_html, "text/html");
    var map_note_dialog = popup_document.body.firstChild;
    
    var map_note_dialog = L.popup()
    .setLatLng(event.latlng)
    .setContent(map_note_dialog)
    .addTo(leaflet_map_note_dialog)
    .openOn(leaflet_map_note_dialog);

    // Place a temporary marker at the location
	temp_marker = L.marker([popup_open_location.lat, popup_open_location.lng]).addTo(leaflet_custom_map_notes);
    temp_marker.setIcon(genTempMarkerIcon());
    //temp_marker.icon = genTempMarkerIcon();

    
    map_note_dialog.on("remove", function() {
        // Save some of the state
        selected_note_icon_index = getSelectedNoteIconIndex();
        selected_note_colour_index = getSelectedColourIndex();
        selected_note_icon_colour = getSelectedNoteColour();

        var picker_element = safeGetId("color-picker-trigger", log);
		picker_element.jscolor.hide();
		picker_element.jscolor = null;
        
        temp_marker.remove();

        leaflet_map_note_dialog.clearLayers();
        log("removed");
        dialog_open = false;
    });


     // Note dialog
    init_note_dialog();
    // Colour picker
    init_colour_picker();
}

function genTempMarkerIcon(label = "") {
    let note = createDiv("overlay map_note web_map_note");
    note.style.fontSize = "10px";
    note.innerHTML = label;

    // Note background
    let note_backg = createDiv("note-background");
    note_backg.style.backgroundColor = darkenRGB(selected_note_icon_colour);

    // Note mask
    let note_mask = createDiv("note-mask");
    note_mask.style = `mask: url('${img_path}/markers/${selected_note_icon_index}.png') no-repeat center / contain; mask-size: 60%; background-color: ${selected_note_icon_colour};`;

    // Note border
    let note_border = createDiv("note-border");
    note_border.style.border = `1px solid ${selected_note_icon_colour}`;

    note.appendChild(note_backg);
    note.appendChild(note_mask);
    note.appendChild(note_border);

    temp_marker_icon = L.divIcon({
        html: note.outerHTML,
        iconSize: [20, 20],
        iconAnchor: [20, 20],
        className: '' // Avoid leaflet's default icon styling
    });

    return temp_marker_icon;
}

function init_note_dialog() {
	log("selected_note_icon_colour is", selected_note_icon_colour);

    // Add listener to apply button
    safeGetId("map-note-apply", log).addEventListener('click', mapNoteApplyClicked);

    // Add listeners to each icon
    const note_icons = document.querySelectorAll(".note-icon");
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");

    // Colour the icons with the initial colour
    if (note_icon_colours.length > 0) {
        const initialColor = note_icon_colours[0].getAttribute("data-current-color");
        setIconColours(note_icons, initialColor);
    }

    // Note icons
    note_icons.forEach((icon) => {
        icon.addEventListener("click", () => {
            deselectAllIcons(note_icons);
            icon.classList.add("selected");
            selected_note_icon_index = icon.getAttribute("index");
            temp_marker.setIcon(genTempMarkerIcon());
        });
    });

    // Note icon colours
    note_icon_colours.forEach((icon) => {
        icon.addEventListener("click", () => {
            deselectAllIcons(note_icon_colours);
            icon.classList.add("selected");
            var selected_colour = icon.getAttribute("data-current-color")
            setIconColours(note_icons, selected_colour);
            selected_note_icon_colour = selected_colour;
            temp_marker.setIcon(genTempMarkerIcon());
        });
    });

    // Use saved selected note icon and colour
    safeGetClassName("note-icon-colour", log)[selected_note_colour_index].classList.add("selected");
    safeGetClassName("note-icon", log)[selected_note_icon_index].classList.add("selected");
	note_icons.forEach((icon) => {
		icon.style.backgroundColor = selected_note_icon_colour;
	});
}


function init_colour_picker() {
    jscolor.install();
    var picker_element = safeGetId("color-picker-trigger", log);
    picker_element.addEventListener("click", function() {
        this.jscolor.show();
    });

    // Set colours of icons
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");
    note_icon_colours.forEach((icon) => { icon.style.backgroundColor = icon.getAttribute("data-current-color")});

    // Colour picker icon
    picker_element.style.background = 'conic-gradient(red, yellow, green, cyan, blue, magenta, red)';
}

// Set icons to colour
function setIconColours(icons, colour) {
    icons.forEach((icon => {
        icon.style.backgroundColor = colour;
    }));
}

// Remove selected class from provided elements
function deselectAllIcons(icons) {
    icons.forEach((i) => i.classList.remove("selected"));
}

function getSelectedNoteIconIndex() {
    const note_icons = Array.from(document.querySelectorAll(".note-icon"));
    return note_icons.findIndex(icon => icon.classList.contains("selected"));
}

function getSelectedColourIndex() {
    const note_icon_colours = Array.from(document.querySelectorAll(".note-icon-colour"));
    return note_icon_colours.findIndex(colour => colour.classList.contains("selected"));
}


function getSelectedNoteColour() {
    const note_icon = safeGetClassName("note-icon", log)[0];
    return rgb2hex(note_icon.style.backgroundColor);
}

function mapNoteApplyClicked() {
    log("CLICKED APPLY");

	log(popup_open_location)
	L.marker([popup_open_location.lat, popup_open_location.lng]).addTo(leaflet_custom_map_notes);

    // Remove the note dialog
    leaflet_map_note_dialog.clearLayers();

    // Send to server here with socketio
}

function pickerColourChange(picker) {
    const new_colour = picker.toHEXString();
    const note_icons = document.querySelectorAll(".note-icon");
    selected_note_icon_colour = new_colour;
    temp_marker.setIcon(genTempMarkerIcon());
    setIconColours(note_icons, new_colour);
}

window.pickerColourChange = pickerColourChange;

const dialog_html = `
	<div id="map-note-dialog" class="map-note-dialog">
	<span style="margin-left:5px">EDIT MARKER</span>
	<div class="map-note-options-container">
		<div class="map-note-options-table">
		<table>
			<tr>
			<th class="note-op-name">NAME</th>
			<th class="note-input-cell">
				<input type="text" id="map-note-label" class="note-input" placeholder="Enter Text..." />
			</th>
			</tr>
			<tr>
			<td class="note-op-name">MARKER</td>
			<td>
				<div class="icon-row">
				<div index="0" class="note-icon" style="mask-image: url('static/images/markers/0.png')"></div>
				<div index="1" class="note-icon" style="mask-image: url('static/images/markers/1.png')"></div>
				<div index="2" class="note-icon" style="mask-image: url('static/images/markers/2.png')"></div>
				<div index="3" class="note-icon" style="mask-image: url('static/images/markers/3.png')"></div>
				<div index="4" class="note-icon" style="mask-image: url('static/images/markers/4.png')"></div>
				<div index="5" class="note-icon" style="mask-image: url('static/images/markers/5.png')"></div>
				</div>
				<!-- Second row of icons -->
				<div class="icon-row">
				<div index="6" class="note-icon" style="mask-image: url('static/images/markers/6.png')"></div>
				<div index="7" class="note-icon" style="mask-image: url('static/images/markers/7.png')"></div>
				<div index="8" class="note-icon" style="mask-image: url('static/images/markers/8.png')"></div>
				<div index="9" class="note-icon" style="mask-image: url('static/images/markers/9.png')"></div>
				<div index="10" class="note-icon" style="mask-image: url('static/images/markers/10.png')"></div>
				<div index="11" class="note-icon" style="mask-image: url('static/images/markers/11.png')"></div>
				</div>
			</td>
			</tr>
			<tr>
			<td class="note-op-name">COLOUR</td>
			<td>
				<div class="icon-row">
				<div id="colour_yellow" class="note-icon-colour" data-current-color="#cbcd53"></div>
				<div id="colour_blue" class="note-icon-colour" data-current-color="#2e66af"></div>
				<div id="colour_green" class="note-icon-colour" data-current-color="#6c9835"></div>
				<div id="colour_red" class="note-icon-colour" data-current-color="#a73533"></div>
				<div id="colour_purple" class="note-icon-colour" data-current-color="#a253ae"></div>
				<div id="color-picker-trigger" class="note-icon-colour note-rainbow-icon" data-current-color="#ab2567" data-jscolor="{value:'#9f3ad7', onInput:'window.pickerColourChange(this)'}">


				</div>
				</div>
			</td>
			</tr>
		</table>
		</div>
		<div id="map-note-apply" class="map-note-apply">APPLY</div>
	</div>
	</div>
`;

function log(...args) {
	if (DEBUG)
		console.log("%c[map_notes.js] ", "color: #a0e02f", ...args);
}