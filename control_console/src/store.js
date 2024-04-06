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

        notifications: [

        ],

        logID: 0,
        log: [

        ]
    },
    mutations: {
        togglePower(state) {
            state.power = !state.power;
        },

        newNotification(state, {message, severity}) {
            state.notifications.push({ message, severity });

            const date = getDateTime();
            const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
            const complete_message = `${log_dateTime} | ${message}`;

            state.log.push({id: state.logID, message: complete_message});

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

            state.log.push({id: state.logID, message: complete_message});
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