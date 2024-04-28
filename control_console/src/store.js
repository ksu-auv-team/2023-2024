// //Google Chart API
google.charts.load('current', {'packages':['corechart']});


import {createStore} from "vuex";

function getDateTime () {
    const currentDate = new Date();
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const time_period = currentDate.getHours() < 12 ? "am" : "pm";

    const month = months[currentDate.getMonth()];
    const day = currentDate.getDate();
    const year = currentDate.getFullYear();
    let hours = currentDate.getHours();
    let minutes = currentDate.getMinutes();

    if (hours > 12) { hours -= 12; }
    if (hours === 0) { hours = 12; }
    if (minutes < 10) { minutes = `0${minutes}`; }

    return {
        month: month,
        day: day,
        year: year,
        hours: hours,
        minutes: minutes,
        time_period: time_period
    };
}

const store = createStore({
    state: {
        currentError: {
            errorCode: null,
            errorMessage: null,
            officialErrorMessage: null
        },

        power: false,

        batteries : [
            { id: 1, voltage: 0, amps: 0 },
            { id: 2, voltage: 0, amps: 0 },
            { id: 3, voltage: 0, amps: 0 },
            { id: 4, voltage: 0, amps: 0 }
        ],

        motors : [
            { id: 1, pwm: 0 },
            { id: 2, pwm: 0 },
            { id: 3, pwm: 0 },
            { id: 4, pwm: 0 },
            { id: 5, pwm: 0 },
            { id: 6, pwm: 0 },
            { id: 7, pwm: 0 },
            { id: 8, pwm: 0 }
        ],

        servos : [
            { id: 1, pwm: 0 },
            { id: 2, pwm: 0 },
        ],

        chartIteration: 1,
        charts: {
            battery_voltage_chart : {
                chart: null,
                chartData: null,
                chartOptions: null,
                subject: "Battery",
                column_count: 4,
                title: "Battery Voltage",
                x_title: "Per Fetch Iteration",
                y_title: "Voltage",
                y_max: 50,
                container_id: 'battery_voltage',
                unit_reference: 0,
                reference_unit: 'voltage',
                selection_bool: false
            },

            battery_amp_chart : {
                chart: null,
                chartData: null,
                chartOptions: null,
                subject: "Battery",
                column_count: 4,
                title: "Battery Amps",
                x_title: "Per Fetch Iteration",
                y_title: "Amps",
                y_max: 30,
                container_id: 'battery_amp',
                unit_reference: 0,
                reference_unit: 'amps',
                selection_bool: false
            },

            motor_chart : {
                chart: null,
                chartData: null,
                chartOptions: null,
                subject: "Motor",
                column_count: 8,
                title: "Motor PWM",
                x_title: "Per Fetch Iteration",
                y_title: "PWM",
                y_max: 100,
                container_id: 'motor_pwm',
                unit_reference: 0,
                reference_unit: 'pwm',
                selection_bool: false
            },

            servo_chart : {
                chart: null,
                chartData: null,
                chartOptions: null,
                subject: 'Servo',
                column_count: 2,
                title: "Servo PWM",
                x_title: "Per Fetch Iteration",
                y_title: "PWM",
                y_max: 100,
                container_id: 'servo_pwm',
                unit_reference: 0,
                reference_unit: 'pwm',
                selection_bool: false
            }
        },

        notifications: [],
        log: []
    },
    mutations: {
        togglePower(state) {
            state.power = !state.power;
            const powerState = state.power ? "ON" : "OFF";
            state.notifications.push({ message: `AUV ${powerState}`, severity: null });

            const date = getDateTime();
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | AUV ${powerState}`;
            state.log.push({message: complete_message,  highlighted: true});
            setTimeout(() => {
                if (state.notifications.length > 0) {
                    state.notifications.shift();
                }
            }, 10000);
        },

        newNotification(state, {message, severity, highlighted}) {
            state.notifications.push({ message, severity });

            const date = getDateTime();
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | ${message}`;

            if(highlighted) {
                state.log.push({message: complete_message, highlighted: highlighted});
            } else {
                state.log.push({message: complete_message, highlighted: false});
            }

            setTimeout(() => {
                if (state.notifications.length > 0) {
                    state.notifications.shift();
                }
            }, 10000);
        },

        addChartData(state) {
            // Ensure that chart.chartData is not null
            const chartArray = [state.charts.battery_voltage_chart, state.charts.battery_amp_chart, state.charts.motor_chart, state.charts.servo_chart]
            chartArray.forEach((chart) => {
                if(chart.chartData === null) {
                    chart.chartData = new google.visualization.DataTable();
                    for (let i = 0; i <= chart.column_count; i++) { //Add first row to create title and subject names
                        if(i === 0) { chart.chartData.addColumn('number', chart.y_title) } else { chart.chartData.addColumn('number', chart.subject + i); }
                    }
                }
            })

            // Get current data from objects and add it to their respective chart data
            // Battery Voltages & Amps
            const batteryVoltages = [state.chartIteration];
            const batteryAmps = [state.chartIteration];
            const motorPWM = [state.chartIteration];
            const servoPWM = [state.chartIteration];
            state.chartIteration++;

            state.batteries.forEach((battery) => {
                batteryVoltages.push(battery.voltage);
                batteryAmps.push(battery.amps);
            })
            state.charts.battery_voltage_chart.chartData.addRow(batteryVoltages);
            state.charts.battery_amp_chart.chartData.addRow(batteryAmps);

            //  Motor PWM
            state.motors.forEach(motor => {
                motorPWM.push(motor.pwm);
            })
            state.charts.motor_chart.chartData.addRow(motorPWM);

            //  Servo PWM
            state.servos.forEach((servo) => {
                servoPWM.push(servo.pwm);
            })
            state.charts.servo_chart.chartData.addRow(servoPWM);

            // If the chart exists on the DOM. Basically check if were on the data page and if the chart exists to update it.
            if(state.charts.battery_voltage_chart.chart !== null) {
                state.charts.battery_voltage_chart.chart.draw(state.charts.battery_voltage_chart.chartData, state.charts.battery_voltage_chart.chartOptions);
                state.charts.battery_amp_chart.chart.draw(state.charts.battery_amp_chart.chartData, state.charts.battery_amp_chart.chartOptions);
                state.charts.motor_chart.chart.draw(state.charts.motor_chart.chartData, state.charts.motor_chart.chartOptions);
                state.charts.servo_chart.chart.draw(state.charts.servo_chart.chartData, state.charts.servo_chart.chartOptions);
            }
        },

        clearChartData(state) {
            const batteryVoltageChart = state.charts.battery_voltage_chart;
            const batteryAmpsChart = state.charts.battery_amp_chart;
            const motorChart = state.charts.motor_chart;
            const servoChart = state.charts.servo_chart;
            const charts = [batteryVoltageChart, batteryAmpsChart, motorChart, servoChart]

            batteryVoltageChart.chartData = null;
            batteryAmpsChart.chartData = null;
            motorChart.chartData = null;
            servoChart.chartData = null;

            charts.forEach((chart) => {
                chart.chartData = new google.visualization.DataTable();
                for (let i = 0; i <= chart.column_count; i++) { //Add first row to create title and subject names
                    if(i === 0) { chart.chartData.addColumn('number', chart.y_title) } else { chart.chartData.addColumn('number', chart.subject + i); }
                }
                chart.chart.draw(chart.chartData, chart.chartOptions);
            })
        },

        newLog(state, message) {
            const date = getDateTime();
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | ${message}`;

            state.log.push({
                message: complete_message,
                highlighted: false
            });
        },
    },

    actions: {
        handleErrors({ dispatch }, error) {
            if(error.request && !error.response) {
                dispatch('relayErrors', {
                    errorCode: '404',
                    errorMessage: `Unable to contact ORIN`,
                    officialErrorMessage: error.message,
                })
            } else if (error.message === "404") {
                dispatch('relayErrors', {
                    errorCode: '404',
                    errorMessage: `Unable to contact ORIN - Connection Severed`,
                    officialErrorMessage: null,
                })
            } else {
                dispatch('relayErrors', {
                    errorCode: '500',
                    errorMessage: `Unable to contact ORIN - Reason Unknown`,
                    officialErrorMessage: null,
                })
            }
        },

        relayErrors({ commit }, {errorCode, errorMessage, officialErrorMessage}) {
            commit('newNotification', {message: `Error Code: ${errorCode} `, severity: 'notification_alert', highlighted: true});
            commit('newLog', `Error Message: ${errorMessage}`);
            if(officialErrorMessage !== null) {
                commit('newLog', `Official Error Message: ${officialErrorMessage}`);
            }
        }
    }

    // mutations: {
    //     setBatteries(state, batteries) {
    //         state.batteries = batteries; // Update the batteries array with the fetched data
    //     }
    // },
    // actions: {
    //     async fetchBatteries({ commit }) {
    //         try {
    //             const response = await axios.get('https://example.com/api/batteries'); // Replace with your API endpoint
    //             const batteries = response.data; // Extract the batteries data from the response
    //             commit('setBatteries', batteries); // Commit a mutation to update the state with the fetched data
    //         } catch (error) {
    //             console.error('Error fetching batteries:', error);
    //         }
    //     }
    // },
})

export default store;