import { my_steam_id } from "./steam.js";

const DEBUG = true;

export function initialiseDialogs() {
    // Colour picker
    init_colour_picker();
    // Note dialog
    init_note_dialog();
}

function init_note_dialog() {
    document.getElementById("map-image").addEventListener('contextmenu', showMapNoteDialog);
    document.getElementById("map-image").addEventListener('click', hideMapNoteDialog);

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
            selectIcon(icon);
        });
    });

    // Note icon colours
    note_icon_colours.forEach((icon) => {
        icon.addEventListener("click", () => {
            deselectAllIcons(note_icon_colours);
            selectIcon(icon);
            setIconColours(note_icons, icon.getAttribute("data-current-color"));
        });
    });
}

function showMapNoteDialog(event) {
	// Prevent the default context menu
	event.preventDefault();
  
	// Get the dialog element and position it at the click location
	var dialog = document.getElementById('map-note-dialog');
    
    var leftPanel = document.getElementById("left-panel");
	dialog.style.left = (event.pageX - leftPanel.offsetWidth) + 'px';
	dialog.style.top = event.pageY + 'px';
	dialog.style.display = 'block';
}

function hideMapNoteDialog(event) {
	var dialog = document.getElementById('map-note-dialog');

    dialog.style.display = 'none';
}


function init_colour_picker() {
    jscolor.install();

    // Set colours of other icons
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");
    note_icon_colours.forEach((icon) => { icon.style.backgroundColor = icon.getAttribute("data-current-color")});

    document.getElementById('color-picker-trigger').style.background = 'conic-gradient(red, yellow, green, cyan, blue, magenta, red)';
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

// Add selected class to provided elements
function selectIcon(icon) {
    icon.classList.add("selected");
}

function mapNoteApplyClicked() {
    const note_icons = Array.from(document.querySelectorAll(".note-icon"));
    const note_icon_colours = Array.from(document.querySelectorAll(".note-icon-colour"));

    let selected_label = document.getElementById("map-note-label").value;

    let selected_icon = note_icons.find((i) => i.classList.contains("selected"));
    let selected_icon_index = selected_icon ? selected_icon.getAttribute("index") : null;
    
    let selected_colour_icon = note_icon_colours.find((i) => i.classList.contains("selected"));
    let selected_colour = selected_colour_icon ? selected_colour_icon.getAttribute("data-current-color") : null;
    
    hideMapNoteDialog();
    var dialog = document.getElementById("map-note-dialog");

    log("Create map note marker at (" + dialog.style.left + ", " + dialog.style.top + ") where icon is " + selected_icon_index + 
            ".png, colour is " + selected_colour + " label is \"" + selected_label + "\" for steam_id " + my_steam_id);

}

function log(...args) {
	if (DEBUG)
		console.log("%c[dialogs.js] ", "color: #a0e02f", ...args);
}