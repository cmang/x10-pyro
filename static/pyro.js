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

function turn_on(house, unit) {
    api_url = `/${house}/${unit}/ON`;
    turn_blinker_on();
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

