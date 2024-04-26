import Api from './api';

const sergiosApi = Api('https://sanchezalvarez.dev/api'); //Do not try to access if not connected to internet
const orinApi = Api('http://192.168.0.1:5000'); //Update to match local DHCP url on local network


export default {


    // POWER FUNCTIONS
    fetchPower() {
        return sergiosApi.get("/auv/power/fetch");
    },

    togglePower() {
        return sergiosApi.post("/auv/power/toggle");
    },

    checkActiveSession() {
        return sergiosApi.get("/auv/log/checkSession");
    }
};