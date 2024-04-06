import {createStore} from "vuex";

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

        log: [

        ]
    },
    mutations: {
        togglePower(state) {
            state.power = !state.power;
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