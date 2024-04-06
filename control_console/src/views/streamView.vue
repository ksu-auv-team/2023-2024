<template>
  <main class="active" id="stream_main">
    <div id="stream">
      <div class="video_stream">
        <div class="stream_header">
          <h2 class="camera_title">Regular View</h2>
        </div>
        <hr>
        <div class="stream_container">
          <img id="camera_feed_1" src="@/assets/svg_icons/disconnected.svg" alt="Regular Stream">
        </div>
      </div>

      <div class="data_container" id="battery_data">
        <div v-for="(battery, index) in batteries" :key="battery.id" :id="'battery_' + (index + 1)" class="battery" :style="{ borderColor: batteryBorderColor(battery) }">
          <h2>Battery {{battery.id}}</h2>
          <p>Voltage: <span class="voltage">{{ battery.voltage }}V</span></p>
          <p>Amps: <span class="amps">{{ battery.amps }}A</span></p>
        </div>
      </div>

      <div class="video_stream">
        <div class="stream_header">
          <h2 class="camera_title">Depth Sensor</h2>
        </div>
        <hr>
        <div class="stream_container">
          <img id="camera_feed_2" src="@/assets/depth_ex.jpg" alt="Depth Sensor">
        </div>
      </div>
    </div>

    <div id="notification_center">
      <p v-for="(notification, index) in notifications" :key="index" :class="notification.severity">{{ notification.message }}</p>
    </div>
  </main>
</template>

<script setup>
import {reactive, ref, watch, watchEffect} from "vue";
  import {useStore} from "vuex";
  const store = useStore();

  const state = reactive(store.state);
  const batteries = ref(state.batteries);
  const notifications = ref(state.notifications);
  const watchAllow = ref(false);

const batteryBorderColor = (battery) => {
  if(battery.voltage > (50*.8)) { // Estimate Battery %. Given that max voltage is 50V
    return "Green";
  } else if(battery.voltage > (50*.3)) {
    return "Darkgoldenrod";
  } else if(battery.voltage > 0) {
    return "Red";
  } else {
    return "White";
  }
};


watchEffect(() => { //Later use server to determine when to allow watch
  if(watchAllow.value) {
    batteries.value.forEach((battery) => {
      if(battery.voltage < (50*.3)) {
        store.commit('newNotification', {message: `Battery ${battery.id} Low`, severity: "notification_alert"});
      }
    });
  }
});

setTimeout(() => {
  watchAllow.value = true;
}, 5500)
</script>