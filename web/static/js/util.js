const DEBUG = true;

export function applyRotation(elementId) {
    let angle = Math.ceil(Math.random() * 360); // Initial angle

    // Function to update rotation
    function update() {
        angle = (angle + 1) % 360; // Increment angle and loop at 360
        const element = document.getElementById(elementId);
        if (element) {
            // Combine rotation with existing transform, preserving position and scale
            const transform = element.style.transform;
            const rotateTransform = `rotate(${angle}deg)`;
            element.style.transform = transform.replace(/rotate\([0-9]+deg\)/, '') + ' ' + rotateTransform;
        }
        requestAnimationFrame(update); // Continue rotation
    }

    update(); // Start rotation
}

export function seconds_since_epoch() {
    return Math.floor(Date.now() / 1000);
}

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

export function awaitVariableSet(checkVariable, interval = 100, timeout = 30000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        (function check() {
            if (checkVariable()) {
                resolve(checkVariable());
            } else if (Date.now() - startTime > timeout) {
                reject(new Error('Timeout'));
            } else {
                setTimeout(check, interval);
            }
        })();
    });
}

function log(...args) {
    if (DEBUG)
        console.log("%c[team.js] ", "color: #FFC0CB", ...args);
}