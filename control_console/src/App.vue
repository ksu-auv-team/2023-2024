<template>
  <header :style="{ backgroundImage: `url(${require('@/assets/banner.png')}` }">
    <nav>
      <router-link to="/">Stream</router-link>
      <router-link to="/data">Data Monitoring</router-link>
      <router-link to="/log">Log</router-link>
    </nav>
    <button id="power_button" @click = 'testApi'>
      <img id="power_svg" src="@/assets/svg_icons/power-off.svg" alt="Power OFF">
    </button>
  </header>

  <router-view ref="currentView" @toggleDialog="toggleDialog"></router-view>

  <span id="example_chart_size"></span>

  <dialog id="dialog">
    <div id="dialog_content">
    </div>
  </dialog>
</template>



<script setup>
  import connection from "@/server/connection";
  import power_on from '@/assets/svg_icons/power-on.svg';
  import power_off from '@/assets/svg_icons/power-off.svg';
  import {useStore} from "vuex";
  import {onMounted, reactive, ref, watchEffect} from "vue";

  const store = useStore();
  const state = reactive(store.state);
  const currentView = ref(null);
  let data_demo;
  const batteries = ref(state.batteries);
  const watchAllow = ref(false);

  const testApi = async () => {
    try {
      console.log(await connection.testAPI());
    } catch (error) {
      if(error.request && !error.response) {
        console.log("Network connection error: ", error);
      } else {
        console.log("Something went wrong: ", error);
      }
    }
  }

  const powerButton = async () => { //Make async when adding http requests
    const power_svg = document.getElementById('power_svg');
    try {
      const fetch = await connection.togglePower()
      const fetchPower = fetch.data.status;
      if (fetchPower) {
        power_svg.src =power_on;
        power_svg.alt = 'Power ON';
      } else {
        power_svg.src = power_off;
        power_svg.alt = 'Power OFF';
        // stopDataDemo();
      }
      let power_status;
      if(state.power === false) {
        power_status = "OFF";
      } else {
        power_status = "ON";
      }

      if(fetchPower !== state.power) { store.commit("togglePower") } else {store.commit('newNotification', {message: `AUV ${power_status}`, highlighted: true});}

    } catch (error) {
      if(error.request && !error.response) {
        console.log("***Not connected to internet. Cannot contact external servers.***");
      } else {
        store.commit("newNotification", {message: "AUV Power Failed"});
        store.commit('newLog', error);
      }
    }
  }

  const getActiveSession = async () => {
    try {
      const session = await connection.checkActiveSession();
      if(session.data !== false) {
        // Update any state variables
        const power = await connection.fetchPower();
        if(power.data.status === true) { updatePowerButton(); }
        // Notify that session has resumed
        store.commit("newNotification", {message: `Session Resumed. Time: ${session.data.date}`, highlighted: false});
      }
    } catch (error) {
      if(error.request && !error.response) {
        console.log("***Not connected to internet. Cannot contact external servers.***");
      } else {
        store.commit("newNotification", {message: "Could not retrieve sessions."});
        store.commit('newLog', error);
      }
    }
  }

  const updatePowerButton = () => {
    const power_svg = document.getElementById('power_svg');
    let power_state = "OFF";
    if(state.power === false) {
      power_svg.src =power_on;
      power_svg.alt = 'Power ON';
      power_state = "ON";
    } else {
      power_svg.src = power_off;
      power_svg.alt = 'Power OFF';
    }
    store.commit("newNotification", {message: `Fetched Power: ${power_state}`, highlighted: true});
  }

  watchEffect(() => { //Later use server to determine when to allow watch
    if(watchAllow.value) {
      batteries.value.forEach((battery) => {
        if(battery.voltage <= (50*.3)) {
          store.commit('newNotification', {message: `Battery ${battery.id} Low`, severity: "notification_alert"});
        }
      });
    }
  });

  setTimeout(() => {
    watchAllow.value = true;
  }, 5500)


  // Later replace with the function to fetch data and call the chart updater
  const startDataDemo = async () => {
    data_demo = setInterval(function() {
      store.state.batteries.forEach(function(battery) {

        battery.voltage = parseFloat((Math.random() * 50).toFixed(2));
        battery.amps = parseFloat((Math.random() * 30).toFixed(2));
      });

      store.state.motors.forEach(function (motor) {
        motor.pwm = Math.floor(Math.random() * 100) + 1;
      });

      store.state.servos.forEach(function (servo) {
        servo.pwm = Math.floor(Math.random() * 100) + 1;
      });

      store.commit('addChartData');
    }, 5000);
    console.log("Timeout Started")
  }

  const  stopDataDemo = () => {
    clearInterval(data_demo);
    console.log("Timeout Stopped")
  }

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

  const dialogOptions  = {
    clearCharts: {
      title: "Clear Charts",
      message: "Are you sure you want to clear the charts? All data related to the charts will be lost.",
      buttons: ["Proceed"], // Button titles should have corresponding function. Closing button is already included
      button_functions: [store.commit.bind(store, 'clearChartData')],
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

  const dialog_active = ref(false);
  function toggleDialog(dialog_request) {
    const dialog = document.getElementById('dialog');
    const dialog_content = document.getElementById('dialog_content');
    let dialog_content_object;
    if(!dialog_active.value) {
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
          newButton.onclick = () => dialogFunctions(dialog_content_object.button_functions[i]);
          dialog_buttons.appendChild(newButton);
        }
        dialog_buttons.id = "dialog_buttons";
        dialog_content.appendChild(dialog_title);
        dialog_content.appendChild(dialog_message);
        if(dialog_content_object.textArea) { dialog_content.appendChild(dialog_text_area); }
        dialog_content.appendChild(dialog_buttons);
      }

      dialog.style.display = 'flex';
      dialog_active.value = true;
    } else {
      dialog.style.display = 'none';
      dialog_active.value =false;
      dialog_content.innerHTML = "";
    }
  }

  function dialogFunctions(newFunction) {
    newFunction();
    toggleDialog();
  }

  function saveCharts() {
    // Check if user left a comment when saving charts
    let userChartComment = "";
    if(dialogOptions.saveCharts.textArea) {
      if(document.getElementById('dialog_text_area').value) {
        userChartComment = "Comments: " + document.getElementById('dialog_text_area').value;
      }
    }


    let chartsHTML = "";
    let chartDivs = document.querySelectorAll('.chart_container');
    chartDivs.forEach((div) => {
      chartsHTML += div.outerHTML;
    })

    let logHTML = "<hr><div style='padding: 0 2rem'> <h2>Log</h2>" +
        "";
    state.log.forEach((log) => {
      if(log.highlighted === true) {
        let pText = "<p style='background-color: #343434; font-size: 1.5rem'>" + log.message + " <span style='color: #E2A300; font-size: 2rem'>&bull;</span></p>"
        logHTML += pText;
      } else {
        let pText = "<p style='font-size: 1.5rem'>" + log.message + "</p>"
        logHTML += pText;
      }
    })
    logHTML += " </div>";

    const date = getDateTime();

    let htmlContent = `<!DOCTYPE html><html lang="en">
        <head>
            <title>KSU AUV Recorded Data</title>
            <header style="width: 100vw; color: white; text-align: center">
                <h1>AUV Data saved at ${date.month} ${date.day}, ${date.year} at ${date.hours}:${date.minutes}${date.time_period}</h1>
                <p style="font-size: 1.25rem">${userChartComment}</p>
            </header>
        </head>
        <body style="background-color: #121212; color: #D1D1D1">
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center;">`;
    htmlContent += chartsHTML;
    htmlContent += `</div><div>`
    htmlContent += logHTML;
    htmlContent += '</div></body></html>';

    let htmlBlob = new Blob([htmlContent], {type: 'text/html'});
    const download_link = document.createElement('a');
    download_link.href = URL.createObjectURL(htmlBlob);
    download_link.download = `${date.year} ${date.month} ${date.day}, ${date.hours}_${date.minutes}_${date.time_period} AUV Data Charts.html`;
    download_link.click();

    toggleDialog();
    toggleDialog();
  }

onMounted(() => {
  // startDataDemo();
  // getActiveSession();
})
</script>