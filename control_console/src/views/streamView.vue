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

    <div id="notification_center"></div>
  </main>
</template>

<script setup>
import {reactive, ref} from "vue";
  import {useStore} from "vuex";
  const store = useStore();

  const state = reactive(store.state);
  const batteries = ref(state.batteries);
</script>