/* Javascript for X10 Pyro remote interface */

var blink_state = true;
var blink_interval;
var dark_theme_switch = true;
var static_ver = '2'

function turn_blinker_on() {
    // console.log("debug: turning blinker color on");
    blinker = document.getElementById('blinker');
    blinker.style.backgroundColor = '#F00';
    blink_interval = window.setInterval(blink, 50);
}

function turn_blinker_off() {
    // console.log("debug: turning blinker color off");
    window.clearInterval(blink_interval);
    blinker = document.getElementById('blinker');
    blinker.style.backgroundColor = '#900';
}

function blink() {
    blinker = document.getElementById('blinker');
    blinker.style.backgroundColor = blink_state ? '#F00' : '#900';
    blink_state = !blink_state;     
}

function dim_up(house, unit) {
    api_url = `/${house}/${unit}/BRT`;
    turn_blinker_on();
    sending_message = `Sending: ${house} ${unit} BRT`
    document.getElementById("last-output").innerHTML = sending_message;
    fetch(api_url)
        .then(response => response.text())
        .then((response) => {
            document.getElementById("last-output").innerHTML = response;
            turn_blinker_off();
        }
        );
}

function dim_down(house, unit) {
    api_url = `/${house}/${unit}/DIM`;
    turn_blinker_on();
    sending_message = `Sending: ${house} ${unit} DIM`
    document.getElementById("last-output").innerHTML = sending_message;
    fetch(api_url)
        .then(response => response.text())
        .then((response) => {
            document.getElementById("last-output").innerHTML = response;
            turn_blinker_off();
        }
        );
}


function turn_on(house, unit) {
    api_url = `/${house}/${unit}/ON`;
    turn_blinker_on();
    sending_message = `Sending: ${house} ${unit} ON`
    document.getElementById("last-output").innerHTML = sending_message;
    fetch(api_url)
        .then(response => response.text())
        .then((response) => {
            document.getElementById("last-output").innerHTML = response;
            turn_blinker_off();
        }
        );
}

function turn_off(house, unit) {
    //api_url = '/c/1/OFF';
    api_url = `/${house}/${unit}/OFF`;
    turn_blinker_on();
    sending_message = `Sending: ${house} ${unit} OFF`
    document.getElementById("last-output").innerHTML = sending_message;
    fetch(api_url)
        .then(response => response.text())
        .then((response) => {
            document.getElementById("last-output").innerHTML = response;
            turn_blinker_off();
        }
        );
}


function load_dark_theme() {
    var theme_css = dark_theme_switch ? 'pyro-dark.css' : 'pyro-dark2.css';
    document.getElementById('theme_css').href = `static/${theme_css}?ver=${static_ver}`;
    dark_theme_switch = !dark_theme_switch;
}

function load_light_theme() {
    document.getElementById('theme_css').href = `static/pyro-light.css?ver=${static_ver}`;
}

function body_loaded() {
    // set some defaults
    document.querySelector('#current-house').value = 'c';
    document.getElementById("device_1_name").innerHTML = 'Living Room Lights';
    document.getElementById('dark_theme_button').onclick = load_dark_theme;
    document.getElementById('light_theme_button').onclick = load_light_theme;
    console.log("test");
    //console.log("fnord!");
}

