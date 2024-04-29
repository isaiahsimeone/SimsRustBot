export function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');

    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

export const rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`

/**
 * Get the current time in seconds since unix epoch
 * @returns {number}
 */
export function timeNow() {
    return Math.floor(Date.now() / 1000);
}

/**
 * Given a number of seconds, return a formatted string
 * in the format XXd YYh ZZm QQs. If the number of days
 * is 0, it is omitted, if the number of hours is 0, it is
 * omitted, etc.
 * @param {number} seconds 
 * @returns Formatted time string
 */
export function formatTime(seconds) {
    // Calculate time components
    const days = Math.floor(seconds / (3600 * 24));
    seconds -= days * 3600 * 24;
    const hours = Math.floor(seconds / 3600);
    seconds -= hours * 3600;
    const minutes = Math.floor(seconds / 60);
    seconds -= minutes * 60;

    // Build the output string
    let timeString = '';

    if (days > 0) timeString += `${days}d `;
    if (hours > 0 || days > 0) timeString += `${hours}h `;
    if (minutes > 0 || hours > 0 || days > 0) timeString += `${minutes}m `;
    timeString += `${seconds}s`;

    return timeString.trim();
}

export function darkenRGB(hex, factor=0.75) {
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


export function createDiv(classList = "") {
    var div = document.createElement("div");
    // Split the classList string into an array of class names
    var classes = classList.split(" ");
    classes.forEach(function(className) {
        if (className.trim() !== "") div.classList.add(className.trim());
    });
    return div;
}

export function safeGetId(id, logFunction) {
    var target = document.getElementById(id);
    if (!target) {
        logFunction("Error from safeGetId: No elements found with id", id);
        return createDiv();
    }
    return target;
}

export function safeGetClassName(classname, logFunction) {
    const elements = document.getElementsByClassName(classname);
    if (!elements || elements.length === 0) {
        logFunction("Error from safeGetClassName: No elements found with class name:", classname);
        return []; // Or handle it differently, such as returning an empty array
    }
    return elements;
}

export function asJSON(jsonString) {
    try {
        return JSON.parse(jsonString);
    } catch (error) {
        log("failed to parse JSON");
        return null;
    }
}

export function validateJSON(jsonString, schema) {
    let data;
    try {
        data = JSON.parse(jsonString);
    } catch (error) {
        return { isValid: false, error: "Invalid JSON format." };
    }

    const errors = [];

    for (const key in schema) {
        if (schema.hasOwnProperty(key)) {
            if (data[key] === undefined) {
                errors.push(`Missing required field: ${key}`);
            } else if (typeof data[key] !== schema[key]) {
                errors.push(`Invalid type for field ${key}: expected ${schema[key]}, got ${typeof data[key]}`);
            }
        }
    }

    return errors.length > 0 ? { isValid: false, errors } : { isValid: true };
}

export function hashObject(obj) {
    let hash = 0;
    let str = JSON.stringify(obj);
    for (let i = 0; i < str.length; i++) {
        hash = (hash << 5) - hash + str.charCodeAt(i);
        hash = hash & hash;
    }
    return hash;
}
