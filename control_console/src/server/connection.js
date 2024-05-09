import Api from './api';

const sergiosApi = Api('https://sanchezalvarez.dev/api'); //Do not try to access if not connected to internet
const orinApi = Api('http://192.168.1.16:5000'); //Update to match local DHCP url on local network (1.16 is my PC @ my house)


export default {


    // DEVELOPMENT FUNCTIONS
    // fetchPower() {
    //     return sergiosApi.get("/auv/power/fetch");
    // },

    togglePower() {
        return sergiosApi.post("/auv/power/toggle");
    },

    checkActiveSession() {
        return sergiosApi.get("/auv/log/checkSession");
    },


    // ORIN API

    testAPI() {
        return orinApi.get("/testAPI");
    },

    handlePower() {
        return orinApi.get("/handlePower");
    },

    fetchPower() {
        return orinApi.get("/fetchPower");
    },

    getInputData() {
        return orinApi.get("/get_input_data");
    },

    getOutputData() {
        return orinApi.get("/get_output_data");
    },

    getSensorData() {
        return orinApi.get("/get_sensor_data");
    },

    postInputData(data) {
        return orinApi.post("/post_input_data", data);
    },

    postOutputData(data) {
        return orinApi.post("/post_output_data", data);
    },

    postSensorData(data) {
        return orinApi.post("/post_sensor_data", data);
    }
};