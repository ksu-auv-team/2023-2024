document.addEventListener("DOMContentLoaded", function() {
// -------------------------------------------- Call Anything That Needs To Be Activated On Page Load Here --------------------------------------------
    createBatteryElements();
    createMotorElements();
    createServoElements();
    initChartProperties();

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

//     -------------------------------------------- GLOBAL VARIABLES  |  START TAB PAGES  --------------------------------------------
function switchTab(tab_index) {
    const stream = document.getElementById('stream_main');
    const data = document.getElementById('data_main');
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

function powerButton() { //Make async when adding post requests
    const power_svg = document.getElementById('power_svg');
    if (!auv_power) { //if off
        // INSERT CODE TO POWER SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // .then
        power_svg.src = '../static/imgs/svg_icons/power-on.svg';
        power_svg.alt = 'Power ON';
        auv_power = true;
        power_on_graphs();
        startDataDemo();
        initial_power = true;
    } else {
        // INSERT CODE TO TURN OFF SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
        // CREATE DIALOG TO MAKE SURE USER WANTS TO POWER OFF
        power_svg.src = '../static/imgs/svg_icons/power-off.svg';
        power_svg.alt = 'Power OFF';
        auv_power = false;
        stopDataDemo();
    }
}

function power_on_graphs() {
    if(!initial_power) {
        timer();
    }
}

//---------------------------------------------- END POWER BUTTON | START DIALOG OPTIONS -----------------------------------------------

const dialogOptions  = {
    clearCharts: {
        title: "Clear Charts",
        message: "Are you sure you want to clear the charts? All data related to the charts will be lost.",
        buttons: ["Proceed"], // Button titles should have corresponding function. Closing button is already included
        button_functions: [clearCharts],
        textArea: false,
        textAreaFunctionIndex: null,
        textAreaMessage: null
    },
    saveCharts: {
        title: "Save Charts",
        message: "Would you like to add any comments? Comments will appear at the top of the page.",
        buttons: ["Proceed"],
        button_functions: [saveCharts],
        textArea: true,
        textAreaFunctionIndex: 0,
        textAreaMessage: null
    }
}

let dialog_active = false;
function toggleDialog(dialog_request) {
    const dialog = document.getElementById('dialog');
    const dialog_content = document.getElementById('dialog_content');
    let dialog_content_object;
    if(!dialog_active) {
        switch (dialog_request) {
            case 'clear_charts':
                dialog_content_object = dialogOptions.clearCharts;
                break;
            case 'save_charts':
                dialog_content_object = dialogOptions.saveCharts;
                break;
            default:
                break;
        }

        if(dialog_content_object) {
            const dialog_title = document.createElement('h1');              dialog_title.innerText = dialog_content_object.title;
            const dialog_message = document.createElement('p');    dialog_message.innerText = dialog_content_object.message
            let dialog_text_area;
            if(dialog_content_object.textArea) {
                dialog_text_area = document.createElement('textarea'); dialog_text_area.id = 'dialog_text_area';
            }
            const dialog_buttons = document.createElement('div');               dialog_buttons.classList.add('dialog_buttons');
            let closingButton = document.createElement('button');
            closingButton.innerText = "Cancel";     closingButton.onclick = toggleDialog;
            dialog_buttons.appendChild(closingButton);
            for(let i = 0; i < dialog_content_object.buttons.length; i++) {
                let newButton = document.createElement('button');
                newButton.innerText = dialog_content_object.buttons[i];
                newButton.onclick = dialog_content_object.button_functions[i];
                dialog_buttons.appendChild(newButton);
            }
            dialog_buttons.id = "dialog_buttons";
            dialog_content.appendChild(dialog_title);
            dialog_content.appendChild(dialog_message);
            if(dialog_content_object.textArea) { dialog_content.appendChild(dialog_text_area); }
            dialog_content.appendChild(dialog_buttons);
        }

        dialog.style.display = 'flex';
        dialog_active = true;
    } else {
        dialog.style.display = 'none';
        dialog_active =false;
        dialog_content.innerHTML = "";
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
        let battery_div_2 = document.getElementById(`battery_${battery_object.id}_${battery_object.id}`);
        battery_div.querySelector('.voltage').textContent = `${battery_object.voltage}V`;
        battery_div.querySelector('.amps').textContent = `${battery_object.amps}A`;
        battery_div_2.querySelector('.voltage').textContent = `${battery_object.voltage}V`;
        battery_div_2.querySelector('.amps').textContent = `${battery_object.amps}A`;
        if(battery_object.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
            battery_div.style.borderColor = "Green"
            battery_div_2.style.borderColor = "Green"
        } else if(battery_object.voltage > (50*.3)) {
            battery_div.style.borderColor = "Darkgoldenrod"
            battery_div_2.style.borderColor = "Darkgoldenrod"
        } else {
            battery_div.style.borderColor = "Red"
            battery_div_2.style.borderColor = "Red"
        }
    })
}

function createBatteryElements() {
    let container = document.getElementById('battery_data');
    let container_2 = document.getElementById('battery_data_2');

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

        let batteryDiv_2 = document.createElement('div');
        batteryDiv_2.className = 'battery';
        batteryDiv_2.id = `battery_${battery.id}_${battery.id}`;
        batteryDiv_2.innerHTML = `
            <h2>Battery ${battery.id}</h2>
            <p>Voltage: <span class="voltage">0V</span></p>
            <p>Amps: <span class="amps">0A</span></p>
        `;
        container_2.appendChild(batteryDiv_2);
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