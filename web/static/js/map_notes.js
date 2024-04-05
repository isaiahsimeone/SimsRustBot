import { my_steam_id, nameFromSteamId } from "./steam.js";
import * as socketio from "./socketio.js";
import { leaflet_map_note_dialog } from "./map.js";

const DEBUG = true;

//TODO: vars here to record selected colour and other stuff when resummoning the popup box

export function initialiseMapNotes() {

}

let selected_note_icon_index = 0;
let selected_note_colour_index = 0;
let selected_note_icon_colour_hex = "#"

function init_note_dialog() {

    // Add listener to apply button
    document.getElementById("map-note-apply").addEventListener('click', mapNoteApplyClicked);

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
        });
    });

    // Note icon colours
    note_icon_colours.forEach((icon) => {
        icon.addEventListener("click", () => {
            deselectAllIcons(note_icon_colours);
            icon.classList.add("selected");
            setIconColours(note_icons, icon.getAttribute("data-current-color"));
        });
    });
}

export function showMapNoteDialog(event) {
    // Destroy map note dialog if it's active
    leaflet_map_note_dialog.clearLayers();
    log(selected_note_colour_index, selected_note_icon_index);
	// Get the dialog element and position it at the click location
	var dialog = document.getElementById('map-note-dialog');
    log(dialog);

    var popup_document = new DOMParser().parseFromString(dialog_html, "text/html");
    var map_note_dialog = popup_document.body.firstChild;
    
    // Use saved selected note icon and colour
    // TODO: save the colour
    map_note_dialog.getElementsByClassName("note-icon-colour")[selected_note_colour_index].classList.add("selected");
    map_note_dialog.getElementsByClassName("note-icon")[selected_note_icon_index].classList.add("selected");


    var map_note_dialog = L.popup()
    .setLatLng(event.latlng)
    .setContent(map_note_dialog)
    .addTo(leaflet_map_note_dialog)
    .openOn(leaflet_map_note_dialog);

    map_note_dialog.on("remove", function() {
        // Save some of the state
        selected_note_icon_index = getSelectedNoteIconIndex();
        selected_note_colour_index = getSelectedColourIndex();

        var picker_element = document.getElementById("color-picker-trigger");
        picker_element.jscolor.hide();
        log("removed");
    });


     // Note dialog
    init_note_dialog();
    // Colour picker
    init_colour_picker();
}



function init_colour_picker() {
    jscolor.install();
    var picker_element = document.getElementById("color-picker-trigger");
    picker_element.addEventListener("click", function() {
        this.jscolor.show();
    });

    // Set colours of icons
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");
    note_icon_colours.forEach((icon) => { icon.style.backgroundColor = icon.getAttribute("data-current-color")});

    // Colour picker icon
    picker_element.style.background = 'conic-gradient(red, yellow, green, cyan, blue, magenta, red)';
}


function updateNoteIconsColor(color) {
    const noteIcons = document.querySelectorAll(".note-icon");
    noteIcons.forEach(icon => {
        icon.style.backgroundColor = color;
    });
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
    const note_icons = document.querySelectorAll(".note-icon");
    for (let i = 0; i < note_icons.length; i++) {
        if (note_icons[i].classList.contains("selected"))
            return i;
    }
    return 0;
}

function getSelectedColourIndex() {
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");
    for (let i = 0; i < note_icon_colours.length; i++) 
        if (note_icon_colours[i].classList.contains("selected"))
            return i;
    return 0;
}

function mapNoteApplyClicked() {
    log("CLICKED APPLY");


    // Remove the note dialog
    leaflet_map_note_dialog.clearLayers();

    // Send to server here with socketio
}


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
              <div id="color-picker-trigger" class="note-icon-colour note-rainbow-icon" data-current-color="#ab2567" data-jscolor="{value:'#9f3ad7', onInput:'pickerColourChange(this)'}">


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