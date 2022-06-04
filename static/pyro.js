/* Javascript for X10 Pyro remote interface */

function turn_blinker_on() {
    // console.log("debug: turning blinker color on");
    blinker = document.getElementById('blinker')
    blinker.style.backgroundColor = '#F00';
}

function turn_blinker_off() {
    // console.log("debug: turning blinker color off");
    blinker = document.getElementById('blinker')
    blinker.style.backgroundColor = '#900';
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

function body_loaded() {
    // set some defaults
    document.querySelector('#current-house').value = 'c';
    document.getElementById("device_1_name").innerHTML = 'Living Room Lights';
    //console.log("fnord!");
}

