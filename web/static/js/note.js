import { positionMarker, mapContainer, panzoom } from "./map.js";
import { img_path } from "./main.js";

const DEBUG = true;


let map_notes = null;
let web_map_notes = [];

const MapNoteColours = {
	0: "#cbcd53",
	1: "#2e66af",
	2: "#6c9835",
	3: "#a73533",
	4: "#a253ae",
	5: "#13d7b0"
}


// Map note type 0 is death marker, type 1 is a player set marker
// These are always the markers of the player running the bot
export function receiveMapNotes(notes) {
	log("I got map notes: " + JSON.stringify(notes));
	map_notes = notes;

	redrawMapNotes();
}

export function receiveWebMapNote(note) {
	log("I received a custom map note: " + JSON.stringify(note));
	web_map_notes.push(note);

	redrawMapNotes();
}

function deleteAllMapNotes() {
	var elements = document.getElementsByClassName("map_note");
	
	Array.from(elements).forEach((element) => {
		element.remove();
	});
}

export function redrawMapNotes() {    
    if (!map_notes)
        return;

	deleteAllMapNotes();

	drawRustServerNotes();
	drawWebNotes();
}

function drawRustServerNotes() {
	for (let i = 0; i < map_notes.length; i++) {
		let note = map_notes[i];
		createMapNote(i, note.x, note.y, note.icon, MapNoteColours[note.colour_index], note.label);
	}
}

function drawWebNotes() {
	// notes added via web
	for (let i = 0; i < web_map_notes.length; i++) {
		let note = web_map_notes[i];
		log("DRAW");
		createMapNote(i, note.x, note.y, note.icon, note.colour, note.label, true);
	}
}


function createMapNote(id, x, y, icon_index, colour, label, web_note=false) {
	console.log("Creating note");
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
        //background-color: #f0f0f0; /* background color */


        let note_mask = document.createElement("div");
        note_mask.className = "note-mask";
        note_mask.style.mask = `url('${img_path}/markers/${icon_index}.png') no-repeat center / contain`; // icon
        note_mask.style.maskSize = "60%";
        note_mask.style.backgroundColor = `${colour}`; // icon colour


        let note_border = document.createElement("div");
        note_border.className = "note-border";
        note_border.style.border = `1px solid ${colour}`; // Colour for border, same as icon
        //border: 2px solid #ff0000; /* color for the border, same as the icon */


        let note_outer_border = document.createElement("div");
        note_outer_border.className = "note-outer-border"; // Just a black border

        note.appendChild(note_backg);
        note.appendChild(note_mask);
        note.appendChild(note_border);
    }
	//note.appendChild(note_outer_border);
	
	mapContainer.appendChild(note);

	
	positionMarker(note.id, x, y, 0, !web_note);
}

function darkenRGB(hex, factor=0.75) {
	const r = parseInt(hex.slice(1, 3), 16);
	const g = parseInt(hex.slice(3, 5), 16);
	const b = parseInt(hex.slice(5, 7), 16);
    
	// Darken the RGB values
	const darkerR = Math.floor(r * (1 - factor));
	const darkerG = Math.floor(g * (1 - factor));
	const darkerB = Math.floor(b * (1 - factor));
  
	// Convert back to hex
	const toHex = (value) => {
	  const hex = value.toString(16);
	  return hex.length == 1 ? '0' + hex : hex;
	};
  
	return `#${toHex(darkerR)}${toHex(darkerG)}${toHex(darkerB)}`;
}

function log(...args) {
	if (DEBUG)
        console.log("%c[note.js] ", "color: #10d6af", ...args);
}