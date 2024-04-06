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

        charts: {
            battery_voltage_chart : {
                chart: 0,
                chartData: null,
                chartOptions: null,
                subject: "Battery",
                column_count: 4,
                title: "Battery Voltage",
                x_title: "Time",
                y_title: "Voltage",
                y_max: 50,
                container_id: 'battery_voltage',
                unit_reference: 0,
                reference_unit: 'voltage',
                selection_bool: false
            },

            battery_amp_chart : {
                chart: 1,
                chartData: null,
                chartOptions: null,
                subject: "Battery",
                column_count: 4,
                title: "Battery Amps",
                x_title: "Time",
                y_title: "Amps",
                y_max: 30,
                container_id: 'battery_amp',
                unit_reference: 0,
                reference_unit: 'amps',
                selection_bool: false
            },

            motor_chart : {
                chart: 2,
                chartData: null,
                chartOptions: null,
                subject: "Motor",
                column_count: 8,
                title: "Motor PWM",
                x_title: "Time",
                y_title: "PWM",
                y_max: 100,
                container_id: 'motor_pwm',
                unit_reference: 0,
                reference_unit: 'pwm',
                selection_bool: false
            },

            servo_chart : {
                chart: 3,
                chartData: null,
                chartOptions: null,
                subject: 'Servo',
                column_count: 2,
                title: "Servo PWM",
                x_title: "Time",
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
            state.log.push({message: `${complete_message}`});
            setTimeout(() => {
                if (state.notifications.length > 0) {
                    state.notifications.shift();
                }
            }, 10000);
        },

        newNotification(state, {message, severity}) {
            state.notifications.push({ message, severity });

            const date = getDateTime();
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | ${message}`;

            state.log.push({message: complete_message});

            setTimeout(() => {
                if (state.notifications.length > 0) {
                    state.notifications.shift();
                }
            }, 10000);
        },

        newLog(state, message) {
            const date = getDateTime;
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | ${message}`;

            state.log.push({message: complete_message});
        }
    },

    actions: {
        async fetchPower({ commit }) {
            try {
                // INSERT CODE TO POWER SUB AND WAIT FOR RESPONSE | HANDLE ERRORS
                // .then
                // const power = fetchedData; then pass it on commit
                commit('togglePower');
            } catch (e) {
                console.error(e);
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