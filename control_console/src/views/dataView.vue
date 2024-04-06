<template>
  <main id="data_main">
    <section>
      <h1>Data Monitoring</h1>
      <div id="data_monitoring">
        <!--            4 batteries(voltage:float | amps: int)  |  8 Motors(pwm: int)  |  3 Servos(pwm: int)     -->
        <div class="data_container" id="battery_data_2">
          <div class="battery" id="battery_1">
            <h2>Battery </h2>
            <p>Voltage: <span class="voltage">{{batteries[0].voltage}}V</span></p>
            <p>Amps: <span class="amps">{{batteries[0].amps}}A</span></p>
          </div>

          <div class="battery" id="battery_2">
            <h2>Battery </h2>
            <p>Voltage: <span class="voltage">{{batteries[1].voltage}}V</span></p>
            <p>Amps: <span class="amps">{{batteries[1].amps}}A</span></p>
          </div>

          <div class="battery" id="battery_3">
            <h2>Battery </h2>
            <p>Voltage: <span class="voltage">{{batteries[2].voltage}}V</span></p>
            <p>Amps: <span class="amps">{{batteries[2].amps}}A</span></p>
          </div>

          <div class="battery" id="battery_4">
            <h2>Battery </h2>
            <p>Voltage: <span class="voltage">{{batteries[3].voltage}}V</span></p>
            <p>Amps: <span class="amps">{{batteries[3].amps}}A</span></p>
          </div>
        </div>

<!--      ----------------------------------------  MOTORS ------------------------------------------>
        <div class="data_container" id="motor_data">
          <div class="motor">
            <h2>Motor 1</h2>
            <p>pwm: {{motors[0].pwm}}%</p>
          </div>

          <div class="motor">
            <h2>Motor 2</h2>
            <p>pwm: {{motors[1].pwm}}%</p>
          </div>

          <div class="motor">
            <h2>Motor 3</h2>
            <p>pwm: {{motors[2].pwm}}%</p>
          </div>

          <div class="motor">
            <h2>Motor 4</h2>
            <p>pwm: {{motors[3].pwm}}%</p>
          </div>
        </div>

<!--      -------------------------------------------  SERVOS  --------------------------------------------->
        <div class="data_container" id="servo_data">
          <div class="servo">
            <h2>Servo 1</h2>
            <p>pwm: {{servos[0].pwm}}%</p>
          </div>

          <div class="servo">
            <h2>Servo 2</h2>
            <p>pwm: {{servos[1].pwm}}%</p>
          </div>

        </div>
      </div>
    </section>

    <section>
      <h1>Data Charts</h1>
      <div id="chart_controls">
        <button onclick="toggleDialog('clear_charts')">Clear Charts</button>
        <button onclick="toggleDialog('save_charts')">Save Charts</button>
      </div>
      <div id="data_charts">
        <div class="chart_container">
          <div id="battery_voltage"></div>
        </div>

        <div class="chart_container">
          <div id="battery_amp"></div>
        </div>

        <div class="chart_container">
          <div id="motor_pwm"></div>
        </div>

        <div class="chart_container">
          <div id="servo_pwm"></div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
  import {useStore} from "vuex";
  import {reactive, ref} from "vue";
  const store = useStore();

  const state = reactive(store.state);
  const batteries = ref(state.batteries);
  const motors = ref(state.motors);
  const servos = ref(state.servos);

  // ------------------------------------------- BATTERIES -------------------------------------------
  const updateBatteryDisplays = () => {
    store.state.batteries.forEach(function (battery_object) {
      let battery_div = document.getElementById(`battery_${battery_object.id}`);
      battery_div.querySelector('.voltage').textContent = `${battery_object.voltage}V`;
      battery_div.querySelector('.amps').textContent = `${battery_object.amps}A`;
      if(battery_object.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
        battery_div.style.borderColor = "Green";
      } else if(battery_object.voltage > (50*.3)) {
        battery_div.style.borderColor = "Darkgoldenrod";
      } else {
        battery_div.style.borderColor = "Red";
        // createNotification(`Battery ${battery_object.id} Low`, 1);
      }
    })
  }
</script>
