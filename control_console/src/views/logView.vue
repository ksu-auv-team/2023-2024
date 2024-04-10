<template>
  <main id="log_main">
    <button id="log_scroll_control" onclick="control_scroll()">
      <img src="@/assets/svg_icons/scroll_pause.svg" alt="Scroll Control">
    </button>

    <p v-for="(log) in logs" :key="logs.indexOf(log)" :id="'log_' + logs.indexOf(log)" class="log_message" :class="{ 'marked': log.highlighted }" @click="highlight_message('log_' + logs.indexOf(log))">
      {{log.message}}
      <span class="highlight_indicator">•</span>
    </p>
  </main>
</template>

<script setup>
  import {useStore} from "vuex";
  import {reactive, ref} from "vue";

  const store = useStore();
  const state = reactive(store.state);
  const logs = ref(state.log);


  const highlight_message = (message_container) => {
    const container = document.getElementById(message_container);
    if(container.classList.contains('marked')) {
      container.classList.remove('marked');
    } else {
      container.classList.add('marked');
    }
    const logIndex = message_container.substring(4);
    logs.value[logIndex].highlighted = logs.value[logIndex].highlighted !== true;
  }

</script>