//@ts-check
import * as socketio from "./socketio.js";
import * as util from "./util.js";

const DEBUG = true;

let devices;

let smart_switch_states;

const ENTITY_TYPE_SMART_SWITCH = "1";

export async function initialiseDeviceManager() {
    devices = (await socketio.request_topic("paired_devices")).devices;
    smart_switch_states = (await socketio.request_topic("smart_switch_states")).switches;
    
    log("got devices:", devices);
    populateSmartSwitchPanel();
    setSmartSwitchOnOff();

}

export function receiveSmartSwitchStates(states) {
    log("got updated smart switch states", states);
    smart_switch_states = states.switches;
    setSmartSwitchOnOff();
}

export function receivePairedDevices(paired_devices) {
    log("got updated paired devices", paired_devices);

    if (devices.length == paired_devices.length) {
        updateSmartSwitchNames();
        setSmartSwitchOnOff();
        devices = paired_devices.devices;
        return ;
    }

    devices = paired_devices.devices;
    // Draw
    populateSmartSwitchPanel();
    log("drawing smart switch panel");
}

function setSmartSwitchOnOff() {
    var switch_eids_with_status = Object.keys(smart_switch_states);
    log("setting switch states", Object.keys(smart_switch_states));
    for (let i = 0; i < switch_eids_with_status.length; i++) {
        var switch_eid = switch_eids_with_status[i];
        setPanelSwitchState(switch_eid);
    }
}

function setPanelSwitchState(eid) {
    log("set ", eid, " to ", smart_switch_states[eid]);
    util.safeGetId(`device-info-input-${eid}`).checked = smart_switch_states[eid];
}

function updateSmartSwitchNames() {
    // Update device names based on ID.
    for (let i = 0; i < devices.length; i++) {
        var entity_id = devices[i]["entityId"];
        util.safeGetId(`device-info-name-${entity_id}`, log).innerHTML = devices[i]["title"];
    }
}


function populateSmartSwitchPanel() {
    var target = util.safeGetId("device-info", log);
    target.innerHTML = "";
    log(typeof(devices));
    for (let i = 0; i < devices.length; i++) {
        log(devices[i]);
        if (devices[i]["entityType"] != ENTITY_TYPE_SMART_SWITCH)
            continue;
        var eid = devices[i]["entityId"];
        target.appendChild(createSmartSwitchPanel(eid, devices[i]["title"]));
        setPanelSwitchState(eid);
    }
}

 

function edit_device_name(element) {
    log("CALLED edit", element);
    let nameSpan = element.querySelector('.device-info-name');
    let input = element.querySelector('.device-info-edit-name');
    input.style.display = 'inline-block'; // Show the input
    input.value = nameSpan.innerText; // Set input value to current text
    nameSpan.style.display = 'none'; // Hide the current name span
    input.focus(); // Focus the input field
}

function set_new_device_name(input) {
    let nameSpan = input.previousElementSibling;
    nameSpan.innerText = input.value; // Update the text
    nameSpan.style.display = 'inline-block'; // Show the text span
    input.style.display = 'none'; // Hide the input field
    
    let eid = input.id.match(/\d+$/)[0];
    if (!eid) {
        log("EID not specified for device?!");
        return ;
    }
    let selected_name = input.previousElementSibling.innerHTML;

    log("changing ", eid, " name to ", selected_name);

    // Publish change via socketio

}

// Expose to entire DOM. So injected elements can call back here
window.editDeviceName = edit_device_name;
window.setNewDeviceName = set_new_device_name;


function createSmartSwitchPanel(eid, name) {


    var device_info_entry = util.createDiv("device-info-entry");
    device_info_entry.id = `device-info-entry-${eid}`;

    var device_info_col1 = util.createDiv("device-info-col");
    var device_info_label = document.createElement("label");
    device_info_label.className = "device-info-switch";
    
    var device_info_input = document.createElement("input");
    device_info_input.id = `device-info-input-${eid}`;
    device_info_input.type = "checkbox";
    device_info_input.checked = false;
    var device_info_slider = document.createElement("span");
    device_info_slider.className = "device-info-slider";
    device_info_slider.classList.add("round"); // needed?

    device_info_label.appendChild(device_info_input);
    device_info_label.appendChild(device_info_slider);
    device_info_col1.appendChild(device_info_label);

    var device_info_col2 = util.createDiv("device-info-col");
    device_info_col2.onclick = function() { window.editDeviceName(this); };

    var device_info_name = util.createDiv("device-info-name");
    device_info_name.id = `device-info-name-${eid}`;
    device_info_name.innerHTML = name;

    var device_info_name_input = document.createElement("input");
    device_info_name_input.type = "text";
    device_info_name_input.id = `device-name-input-${eid}`;
    device_info_name_input.className = "device-info-edit-name";
    device_info_name_input.onblur = function() { window.setNewDeviceName(this); };
    device_info_name_input.style.display = "none";

    device_info_col2.appendChild(device_info_name);
    device_info_col2.appendChild(device_info_name_input);

    device_info_entry.appendChild(device_info_col1);
    device_info_entry.appendChild(device_info_col2);

    return device_info_entry;
}


/**
 * Log a message for this class, if the DEBUG variable is defined.
 * @param  {...any} args A variable number of objects to include in the log
 */
function log(...args) {
	if (DEBUG)
        console.log("%c[device_manager.js] ", "color: #feca88", ...args);
}