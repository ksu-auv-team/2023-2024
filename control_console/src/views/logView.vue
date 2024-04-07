<template>
  <main id="log_main">
    <button id="log_scroll_control" onclick="control_scroll()">
      <img src="@/assets/svg_icons/scroll_pause.svg" alt="Scroll Control">
    </button>

    <p v-for="(log) in logs" :key="logs.indexOf(log)" :id="'log_' + logs.indexOf(log)" class="log_message" @click="highlight_message('log_' + logs.indexOf(log))">
      {{log.message}}
      <span class="highlight_indicator">•</span>
      <label class="log_comment">
        <input type="text" placeholder="Comment Area">
      </label>
    </p>
  </main>
</template>

<script setup>
  import {useStore} from "vuex";
  import {reactive, ref, watchEffect} from "vue";

  const store = useStore();
  const state = reactive(store.state);
  const logs = ref(state.log);
  const scroll_paused = ref(false);
  const log_main = document.getElementById("log_main");


  const highlight_message = (message_container) => {
    const container = document.getElementById(message_container);
    if(container.classList.contains('marked')) { container.classList.remove('marked');
    } else { container.classList.add('marked'); }
  }
  //
  // const control_scroll = () => {
  //   scroll_paused.value = !scroll_paused.value;
  //   if(!scroll_paused.value) {
  //     document.getElementById('log_scroll_control').querySelector('img').src = "@/assets/svg_icons/scroll_pause.svg";
  //   } else {
  //     document.getElementById('log_scroll_control').querySelector('img').src = "@/assets/svg_icons/scroll_down.svg";
  //   }
  // }
  //
  // const scrollLogDown = () => {
  //   if(log_main.scrollHeight > log_main.clientHeight) { document.getElementById('log_scroll_control').style.display = 'initial'; }
  //   if(!scroll_paused.value) { log_main.scrollTop = log_main.scrollHeight; }
  // }

</script>