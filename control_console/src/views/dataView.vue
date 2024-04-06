<template>
  <main id="data_main">
    <section>
      <h1>Data Monitoring</h1>
      <div id="data_monitoring">
        <!--            4 batteries(voltage:float | amps: int)  |  8 Motors(pwm: int)  |  3 Servos(pwm: int)     -->
        <div class="data_container" id="battery_data_2">
          <div v-for="(battery, index) in batteries" :key="battery.id" :id="'battery_' + (index + 1)" class="battery" :style="{ borderColor: batteryBorderColor(battery) }">
            <h2>Battery</h2>
            <p>Voltage: <span class="voltage">{{ battery.voltage }}V</span></p>
            <p>Amps: <span class="amps">{{ battery.amps }}A</span></p>
          </div>
        </div>

<!--      ----------------------------------------  MOTORS ------------------------------------------>
        <div class="data_container" id="motor_data">
          <div v-for="(motors, index) in motors" :key="motors.id" :id="'motor_' + (index + 1)" class="motor">
            <h2>Motor 1</h2>
            <p>pwm: {{motors.pwm}}%</p>
          </div>
        </div>

<!--      -------------------------------------------  SERVOS  --------------------------------------------->
        <div class="data_container" id="servo_data">
          <div v-for="(servos, index) in servos" :key="servos.id" :id="'servo_' + (index + 1)" class="servo">
            <h2>Servo 1</h2>
            <p>pwm: {{servos.pwm}}%</p>
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

  const batteryBorderColor = (battery) => {
    if(battery.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
      return "Green";
    } else if(battery.voltage > (50*.3)) {
      return "Darkgoldenrod";
    } else if(battery.voltage > 0) {
      return "Red";
      // createNotification(`Battery ${battery_object.id} Low`, 1);
    } else {
      return "White";
    }
  };
</script>
