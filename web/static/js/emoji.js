//@ts-check
import { shortname_to_id } from "./structures.js";

const DEBUG = true;

const emojis = new Set([
    "angry", "coffeecan", "cool", "dance", "eyebrow", "eyes", "funny", 
    "happy", "heart", "heartrock", "laugh", "light", "love", "mask", 
    "nervous", "neutral", "scientist", "skull", "smilecry", "trumpet", 
    "wave", "worried", "yellowpin"
]);

/**
 * Count the number of characters used in a string to specify an emoji.
 * e.g. HELLO:a:HELLO -> 3 (:, a, and :)
 * The same logic applies for multiple emoji definitions
 * @param {string} text The text to check
 * @returns The number of characters used to specify an emoji,
 */
export function countEmojiCharacters(text) {
    return [...text.matchAll(/:([^:]+):/g)].reduce((total, match) => total + match[0].length, 0);
}

/**
 * Replace emojis in a given text string with a span containing
 * the image for that emoji
 * @param {string} text The text to replace emoji declarations in
 * @returns The HTML string, potentially with a span with an emoji image
 */
export function emojifyText(text) {
    return text.replace(/:([^:]+):/g, (_, emoji_name) => createEmojiImageSpan(getEmojiFilePath(emoji_name)));
}

/**
 * Search for an emoji image by its name. First, the emojis set is checked,
 * if nothing is found, the set of rust images is checked (by shortname).
 * If neither are found, an empty string is returned
 * @param {string} emoji_name The name of the emoji without colons (e.g. angry, happy) 
 * @returns The path to the emoji image file, or null
 */
function getEmojiFilePath(emoji_name) {
    if (emojis.has(emoji_name))
        return `static/images/emojis/${emoji_name}`;
    else if (shortname_to_id.has(emoji_name))
        return `static/images/items/${shortname_to_id.get(emoji_name)}`;
    return "";
}

/**
 * Create a span containing an emoji image, based on the filepath to that image
 * @param {string} filePath the path to the emoji image 
 * @returns 
 */
function createEmojiImageSpan(filePath) {
    return filePath ? `<span class="rust-emoji-image" style="background-image: url(${filePath}.png);"></span>` : "";
}

function log(...args) {
    if (DEBUG) console.log("%c[emoji.js] ", "color: #f27009", ...args);
}
