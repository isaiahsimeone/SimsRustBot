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