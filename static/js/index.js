document.addEventListener("DOMContentLoaded", function() {
// -------------------------------------------- Call Anything That Needs To Be Activated On Page Load Here --------------------------------------------
    createBatteryElements();
    createMotorElements();
    createServoElements();
    initChartProperties();
    startDataDemo();

    // //Google Chart API
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(data_charts); //Call main chart initializer


//     GET REQUESTS ON LOAD (in-case user refreshes page or auv is already powered on)
})
let data_demo
let timeActive = 0;
function timer() { //later, call this after the api
    setInterval(() => {
        timeActive += 2;
        updateCharts([battery_voltage_chart, battery_amp_chart, motor_chart, servo_chart]);
    }, 5500);
}

// ---------------------------------------- GLOBAL VARIABLES ----------------------------------------
const batteryMaxVoltage = 50;
const batteryMaxAmps = 30;

const motorMaxPWM = 100;

//     -------------------------------------------- GLOBAL VARIABLES  |  START TAB PAGES  --------------------------------------------
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

//     -------------------------------------------- GLOBAL VARIABLES  |  START POWER BUTTON --------------------------------------------
let auv_power = false; //False = off
let initial_power = false;

function power() { //Make async when adding post requests
    const power_svg = document.getElementById('power_svg');
    if (!auv_power) { //if off
        // INSERT CODE TO POWER SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // .then
        power_svg.src = '../static/imgs/svg_icons/power-on.svg';
        power_svg.alt = 'Power ON';
        auv_power = true;
        power_on_graphs();
        initial_power = true;
    } else {
        // INSERT CODE TO TURN OFF SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // CREATE DIALOG TO MAKE SURE USER WANTS TO POWER OFF
        power_svg.src = '../static/imgs/svg_icons/power-off.svg';
        power_svg.alt = 'Power OFF';
        auv_power = false;
    }
}

function power_on_graphs() {
    if(!initial_power) {
        timer();
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
// ------------------------ END SERVO DATA | START LOG PAGE  ----------------------------

function highlight_message(message_container) {
    if(message_container.classList.contains('marked')) { message_container.classList.remove('marked');
    } else { message_container.classList.add('marked'); }
}


//  -----------------------------------------START DATA DEMO -----------------------------------------

function startDataDemo() {
    data_demo = setInterval(function() {
        batteries.forEach(function(battery) {

            battery.voltage = parseFloat((Math.random() * 50).toFixed(2));
            battery.amps = parseFloat((Math.random() * 30).toFixed(2));
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