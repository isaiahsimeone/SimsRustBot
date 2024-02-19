import { positionMarker, mapContainer } from "./map.js";
import { img_path } from "./main.js";

const DEBUG = true;


let map_notes = null;

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

	for (let i = 0; i < map_notes.length; i++) {
		createMapNote(i, map_notes[i]);
	}
}


function createMapNote(id, map_note) {
	if (map_note.type == 0) // death marker
		return ;
	console.log("Creating note");
	let note = document.createElement("div");
	note.className = "overlay map_note";
	note.id = "overlay_note" + id;

	note.style.fontSize = "10px";
	note.innerHTML = map_note.label;
	//note.style.backgroundImage = `url('${img_path}/markers/bed.png')`;


	let icon_colour = MapNoteColours[map_note.colour_index];
	
    if (map_note.icon == 0) {
        note.style.mask = `url('${img_path}/markers/${map_note.icon}.png') no-repeat center / contain`; // icon
        note.style.backgroundColor = `${icon_colour}`; // icon colour
    } else {

        let note_backg = document.createElement("div");
        note_backg.className = "note-background";
        note_backg.style.backgroundColor = darkenRGB(icon_colour);//"#40411a"; // background colour
        //background-color: #f0f0f0; /* background color */


        let note_mask = document.createElement("div");
        note_mask.className = "note-mask";
        note_mask.style.mask = `url('${img_path}/markers/${map_note.icon}.png') no-repeat center / contain`; // icon
        note_mask.style.maskSize = "60%";
        note_mask.style.backgroundColor = `${icon_colour}`; // icon colour


        let note_border = document.createElement("div");
        note_border.className = "note-border";
        note_border.style.border = `1px solid ${icon_colour}`; // Colour for border, same as icon
        //border: 2px solid #ff0000; /* color for the border, same as the icon */


        let note_outer_border = document.createElement("div");
        note_outer_border.className = "note-outer-border"; // Just a black border

        note.appendChild(note_backg);
        note.appendChild(note_mask);
        note.appendChild(note_border);
    }
	//note.appendChild(note_outer_border);
	
	mapContainer.appendChild(note);

	positionMarker(note.id, map_note.x, map_note.y);
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