//function hideDialog() {
//    var dialog = document.getElementById("place-marker-dialog");
//    dialog.style.display = "none";
//}

$(document).ready(function () {
    // Note dialog
    
    init_note_dialog();
    
    
});

function init_note_dialog() {


    // Add listeners to each icon
    const note_icons = document.querySelectorAll(".note-icon");
    const note_icon_colours = document.querySelectorAll(".note-icon-colour");
    
    // Colour the icons with the initial colour
    setIconColours(note_icons, note_icon_colours[0].style.backgroundColor);

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
            setIconColours(note_icons, icon.style.backgroundColor);
        });
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

// Add selected class to provided elements
function selectIcon(icon) {
    icon.classList.add("selected");
}