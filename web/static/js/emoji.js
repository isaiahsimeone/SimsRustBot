//@ts-check


const DEBUG = true;

const emojis = new Set([
    "angry",
    "coffeecan",
    "cool",
    "dance",
    "eyebrow",
    "eyes",
    "funny",
    "happy",
    "heart",
    "heartrock",
    "laugh",
    "light",
    "love",
    "mask",
    "nervous",
    "neutral",
    "scientist",
    "skull",
    "smilecry",
    "trumpet",
    "wave",
    "worried",
    "yellowpin"
]);

export function emojifyText(text) {
    // Match :sometext:
    const regex = /:([^:]+):/g;

    const replacedString = text.replace(regex, (match, emoji_name) => {
        let emoji_filepath = getEmojiFilePath(emoji_name);
        let emoji_image = document.createElement("span");
        emoji_image.style.backgroundImage = `url("${emoji_filepath}.png")`;
        return `<span class="rust-emoji-image" style="background-image: url(${emoji_filepath}.png);"></span>`;
    });
    
    return replacedString;
}

function getEmojiFilePath(emoji_name) {
    if (emojis.has(emoji_name))
        return "static/images/emojis/" + emoji_name;
}

/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[emoji.js] ", "color: #f27009", ...args);
}