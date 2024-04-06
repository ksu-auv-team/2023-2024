<template>
  <header>
    <nav>
      <router-link to="/">Stream</router-link>
      <router-link to="/data">Data Monitoring</router-link>
      <router-link to="/log">Log</router-link>
      <button id="save_data">Save Data</button>
    </nav>
    <button id="power_button" @click = 'powerButton'>
      <img id="power_svg" src="@/assets/svg_icons/power-off.svg" alt="Power OFF">
    </button>
  </header>

  <router-view ref="currentView"></router-view>

  <span id="example_chart_size"></span>

  <dialog id="dialog">
    <div id="dialog_content">
    </div>
  </dialog>
</template>



<script setup>
  import power_on from '@/assets/svg_icons/power-on.svg';
  import power_off from '@/assets/svg_icons/power-off.svg';
  import {useStore} from "vuex";
  import router from "@/router";
  import {getCurrentInstance, onMounted, ref} from "vue";

  const store = useStore();
  const currentView = ref(null)
  let data_demo;

  const powerButton = () => { //Make async when adding post requests
    store.commit("togglePower")

    const power_svg = document.getElementById('power_svg');
    if (store.state.power) {
      power_svg.src =power_on;
      power_svg.alt = 'Power ON';
      // power_on_graphs();
      // startDataDemo();
      // createNotification("AUV Powered ON");
    } else {
      power_svg.src = power_off;
      power_svg.alt = 'Power OFF';
      // stopDataDemo();
      // createNotification("AUV Powered OFF");
    }
  }

  const startDataDemo = () => {
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

    }, 5000);
    console.log("Timeout Started")
  }

  const  stopDataDemo = () => {
    clearInterval(data_demo);
    console.log("Timeout Stopped")
  }

  const dialogOptions  = {
    clearCharts: {
      title: "Clear Charts",
      message: "Are you sure you want to clear the charts? All data related to the charts will be lost.",
      buttons: ["Proceed"], // Button titles should have corresponding function. Closing button is already included
      // button_functions: [clearCharts],
      textArea: false,
      textAreaFunctionIndex: null,
      textAreaMessage: null
    },
    saveCharts: {
      title: "Save Charts",
      message: "Would you like to add any comments? Comments will appear at the top of the page.",
      buttons: ["Proceed"],
      // button_functions: [saveCharts],
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

onMounted(() => {
  startDataDemo()
})
</script>