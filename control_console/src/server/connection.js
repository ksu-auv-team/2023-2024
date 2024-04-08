import Api from './api';

export default {


    // POWER FUNCTIONS
    fetchPower() {
        return Api().get("/auv/power/fetch");
    },

    togglePower() {
        return Api().post("/auv/power/toggle");
    }
};