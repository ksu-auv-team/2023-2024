document.addEventListener("DOMContentLoaded", function() {
// -------------------------------------------- Call Anything That Needs To Be Activated On Page Load Here --------------------------------------------
    createBatteryElements();
    createMotorElements();
    createServoElements();
    startDataDemo();


    // //Google Chart API
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(data_charts); //Call main chart initializer

    timer();

//     GET REQUESTS ON LOAD (in-case user refreshes page or auv is already powered on)
})

let timeActive = 0;
function timer() {
    setInterval(() => {
        timeActive += 2;
        updateBatteryData();
    }, 4000);
}

// ---------------------------------------- GLOBAL VARIABLES ----------------------------------------
const numberOfBatteries = 4;
const batteryMaxVoltage = 50;
const batteryMaxAmps = 30;



// -------------------------------------------- TESTING WEBCAM   --------------------------------------------

let webcam_on = false;
let webcamStream;

function test_webcam(camera_identifier) {
    if (!webcam_on) { //Start webcam
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                let webcam = document.getElementById(`camera_feed_${camera_identifier}`);
                webcam.srcObject = stream;
                webcamStream = stream;
            })
            .catch(function (err) {
                console.error('Unable to transmit camera feed: ', err);
            });
        webcam_on = true;
    } else { //Turn off webcam
        let webcam = document.getElementById(`camera_feed_1`);
        let webcam_2 = document.getElementById(`camera_feed_2`);
        webcam.srcObject = null;
        webcam_2.srcObject = null;
        if (webcamStream) {
            let tracks = webcamStream.getTracks();
            tracks.forEach(function (track) {
                track.stop();
            });
        }
        webcam_on = false;
    }
}

//     -------------------------------------------- END TESTING WEBCAM  |  START TAB PAGES  --------------------------------------------

function switchTab(tab_index) {
    const stream = document.getElementById('stream_main');
    const data = document.getElementById('data_dialog');
    const log = document.getElementById('log_main');

    document.getElementById('stream_tag').classList.remove('active-tab');
    document.getElementById('data_tag').classList.remove('active-tab');
    document.getElementById('log_tag').classList.remove('active-tab');
    if (tab_index === 1) {
        stream.setAttribute("hidden", "true");
        log.setAttribute('hidden', 'true');
        data.removeAttribute('hidden');
        document.getElementById('data_tag').classList.add('active-tab');
    } else if (tab_index === 2) {
        stream.setAttribute("hidden", "true");
        data.setAttribute('hidden', 'true');
        log.removeAttribute('hidden');
        document.getElementById('log_tag').classList.add('active-tab');
    } else {
        data.setAttribute('hidden', 'true');
        log.setAttribute("hidden", "true");
        stream.removeAttribute('hidden');
        document.getElementById('stream_tag').classList.add('active-tab');
    }
}


//     -------------------------------------------- END TAB PAGES  |  START MESSAGE CENTER  --------------------------------------------

function Message(severity, source, message) {
    this.severity =  severity;
    this.source= source;
    this.message  = message;
    this.toString = function () {
        return `Severity: ${this.severity}  |  Source: ${this.source}  |  Message: ${this.message}\n`
    }
}

let message_log = [];

function newMessage(severity, source, message) {
    let new_message = new Message(severity, source, message);
    message_log.push(new_message);
    displayMessage(new_message);
    message_timeout();
}

function message_timeout() {
    const message_center = document.getElementById('messages');

    setTimeout(() => {
        if (message_center.firstChild) {
            message_center.firstElementChild.classList.add('single_message_clear');
        }
    }, 3000)

    setTimeout(() => {
        if (message_center.firstChild) {
            message_center.firstChild.remove();
        }
    }, 4000)
}

function displayMessage(message_data) {
    const message_container = document.createElement('div');
    message_container.classList.add('single_message');

    if(message_data.severity === 1) { message_container.classList.add('warning') }
    if(message_data.severity >= 2) { message_container.classList.add('alert') }

    const title = document.createElement("h3");
    title.innerText = message_data.source;

    const message_message = document.createElement("p");
    message_message.innerText = message_data.message;

    message_container.appendChild(title);
    message_container.appendChild(message_message)

    const message_center = document.getElementById('messages');
    message_center.appendChild(message_container);
}


//     -------------------------------------------- END MESSAGE CENTER  |  START POWER BUTTON --------------------------------------------

let auv_power = false; //False = off

function power() { //Make async when adding post requests
    const power_svg = document.getElementById('power_svg');
    if (!auv_power) { //if off
        // INSERT CODE TO POWER SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // .then
        power_svg.src = '../static/imgs/svg_icons/power-on.svg';
        power_svg.alt = 'Power ON';
        auv_power = true;
    } else {
        // INSERT CODE TO TURN OFF SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // CREATE DIALOG TO MAKE SURE USER WANTS TO POWER OFF
        power_svg.src = '../static/imgs/svg_icons/power-off.svg';
        power_svg.alt = 'Power OFF';
        auv_power = false;
    }
}


//     -------------------------------------------- END POWER BUTTON  |  START BATTERY DATA  --------------------------------------------



const batteries = [
    { id: 1, voltage: 0, amps: 0 },
    { id: 2, voltage: 0, amps: 0 },
    { id: 3, voltage: 0, amps: 0 },
    { id: 4, voltage: 0, amps: 0 }
]

function updateBatteryDisplays() {
    batteries.forEach(function (battery_object) {
        let battery_div = document.getElementById(`battery_${battery_object.id}`);
        battery_div.querySelector('.voltage').textContent = battery_object.voltage;
        battery_div.querySelector('.amps').textContent = battery_object.amps;
        if(battery_object.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
            battery_div.style.borderColor = "Green"
        } else if(battery_object.voltage > (50*.3)) {
            battery_div.style.borderColor = "Darkgoldenrod"
        } else {
            battery_div.style.borderColor = "Red"
        }
    })
}

function createBatteryElements() {
    let container = document.getElementById('battery_data');

    batteries.forEach(function(battery) {
        let batteryDiv = document.createElement('div');
        batteryDiv.className = 'battery';
        batteryDiv.id = 'battery_' + battery.id;
        batteryDiv.innerHTML = `
            <h2>Battery ${battery.id}</h2>
            <p>Voltage: <span class="voltage"></span></p>
            <p>Amps: <span class="amps"></span></p>
        `;
        container.appendChild(batteryDiv);
    });
}

function resetBatteryElements() {
    document.getElementById('battery_data').innerHTML = "";
    createBatteryElements();
}

// Battery Google Area Chart
function battery_chart() {

}

//     -------------------------------------------- END BATTERY DATA  |  START MOTOR DATA  --------------------------------------------

const motors = [
    { id: 1, pwm: 0 },
    { id: 2, pwm: 0 },
    { id: 3, pwm: 0 },
    { id: 4, pwm: 0 },
    { id: 5, pwm: 0 },
    { id: 6, pwm: 0 },
    { id: 7, pwm: 0 },
    { id: 8, pwm: 0 }
]

function updateMotorDisplays() {
    motors.forEach(function (motor_object) {
        let motor_div = document.getElementById(`motor_${motor_object.id}`);
        motor_div.querySelector('.pwm').textContent = motor_object.pwm;
    })
}

function createMotorElements() {
    let container = document.getElementById('motor_data');

    motors.forEach(function(motor) {
        let batteryDiv = document.createElement('div');
        batteryDiv.className = 'motor';
        batteryDiv.id = 'motor_' + motor.id;
        batteryDiv.innerHTML = `
            <h2>Motor ${motor.id}</h2>
            <p>pwm: <span class="pwm">0</span>%</p>
        `;
        container.appendChild(batteryDiv);
    });
}

function resetMotorElements() {
    document.getElementById('battery_data').innerHTML = "";
    createMotorElements();
}


//     -------------------------------------------- END MOTOR DATA  |  START SERVO DATA  --------------------------------------------


const servos = [
    { id: 1, pwm: 0 },
    { id: 2, pwm: 0 },
]

function updateServoDisplays() {
    servos.forEach(function (servo_object) {
        let servo_div = document.getElementById(`servo_${servo_object.id}`);
        servo_div.querySelector('.pwm').textContent = servo_object.pwm;
    })
}

function createServoElements() {
    let container = document.getElementById('servo_data');

    servos.forEach(function(servo) {
        let servo_div = document.createElement('div');
        servo_div.className = 'servo';
        servo_div.id = 'servo_' + servo.id;
        servo_div.innerHTML = `
            <h2>Servo ${servo.id}</h2>
            <p>pwm: <span class="pwm">0</span>%</p>
        `;
        container.appendChild(servo_div);
    });
}

function resetServoElements() {
    document.getElementById('battery_data').innerHTML = "";
    createBatteryElements();
}


//     -------------------- END SERVO DATA | START DATA CHARTS  --------------------

// Battery Chart
let batteryData;
let batteryOptions;
let batteryChart;
function initBatteryChart() {
    let computedSize = window.getComputedStyle(document.getElementById('example_chart_size')) ;
    console.log(parseInt(computedSize.getPropertyValue('height')))
    batteryData = google.visualization.arrayToDataTable([
        ['3 Second Interval', 'Battery1', 'Battery2', 'Battery3', 'Battery4'],
        [0,0,0,0,0]
    ]);
    batteryOptions = {
        backgroundColor: "#343434",
        title: "Battery Voltage",
        titleTextStyle: {color: "white"},
        legend: {textStyle: {color: "#FFFFFF"}, position: 'in'},
        hAxis: {title: '3 Second Interval',titleTextStyle: {color: "white"}, textStyle: {color: "white"}, baselineColor: "white", gridLines: {color: "#FFFFFF"}},
        vAxis: {title: 'Voltage',titleTextStyle: {color: "white"}, textStyle: {color: "white"}, minValue: 0, maxValue: (batteryMaxVoltage+10)},
        width: parseInt(computedSize.getPropertyValue('width')),
        height: parseInt(computedSize.getPropertyValue('height')),
        chartArea: {width: '70%', height: '85%', left: 70, right: 25},
        explorer: {
            actions: ['dragToZoom', 'rightClickToReset'],
            axis: 'horizontal',
            keepInBounds: true,
            maxZoomIn: 10
        }
    }

    batteryChart = new google.visualization.AreaChart(document.getElementById('battery_voltage'));
    batteryChart.draw(batteryData, batteryOptions);
}
function updateBatteryData() { //Call this function per get/post request on .then
    let newInsert = [timeActive];
    batteries.forEach(function(battery) {
        newInsert.push(battery.voltage);
    });
    batteryData.addRow(newInsert);
    batteryChart.draw(batteryData, batteryOptions);
}


function data_charts() {
    console.log("Loaded")
    initBatteryChart();
}

// ------------------------------------------------- LOG PAGE -------------------------------------------------

function highlight_message(message_container) {
    if(message_container.classList.contains('marked')) { message_container.classList.remove('marked');
    } else { message_container.classList.add('marked'); }
}


//  -----------------------------------------START DATA DEMO -----------------------------------------

let data_demo
function startDataDemo() {
    data_demo = setInterval(function() {
        batteries.forEach(function(battery) {

            battery.voltage = parseFloat((Math.random() * 50).toFixed(2));
            battery.amps = parseFloat((Math.random() * 50).toFixed(2));
        });

        motors.forEach(function (motor) {
            motor.pwm = Math.floor(Math.random() * 100) + 1;
        });

        servos.forEach(function (servo) {
            servo.pwm = Math.floor(Math.random() * 100) + 1;
        });

        updateMotorDisplays();
        updateBatteryDisplays();
        updateServoDisplays();
    }, 5000);
    console.log("Timeout Started")
}

function  stopDataDemo() {
    clearInterval(data_demo);
    console.log("Timeout Stopped")
}