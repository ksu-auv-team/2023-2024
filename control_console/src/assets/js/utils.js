import router from "@/router";

const getDateTime = () => {
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

export const checkRoute = (route) => {
    const currentRoutePath = router.currentRoute.value.path;
    return currentRoutePath === route;
};

export default {
    getDateTime,
    checkRoute
}