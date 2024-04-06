<template>
  <main id="log_main">
    <button id="log_scroll_control" onclick="control_scroll()">
      <img src="@/assets/svg_icons/scroll_pause.svg" alt="Scroll Control">
    </button>
  </main>
</template>

<script setup>
  import getDateTime from '@/assets/js/utils';

  const highlight_message = (message_container) => {
    if(message_container.classList.contains('marked')) { message_container.classList.remove('marked');
    } else { message_container.classList.add('marked'); }
  }

  const createLog = (message) => {
    const date = getDateTime;
    const log_dateTime = `${date.month} ${date.day}, ${date.hours}:${date.minutes}${date.time_period}`;
    const complete_message = `${log_dateTime} | ${message}`;

    const log_message = document.createElement('p');
    log_message.classList.add('log_message');
    log_message.onclick = function () { highlight_message(log_message); }
    log_message.innerHTML = `
          ${complete_message}
          <span class="highlight_indicator">•</span>
          <label class="log_comment">
              <input type="text" placeholder="Comment Area">
          </label>
      `
    const log_main = document.getElementById('log_main');
    log_main.appendChild(log_message);

    scrollLogDown();
  }
  let scroll_paused = false;

  const control_scroll = () => {
    scroll_paused = !scroll_paused;
    if(!scroll_paused) {
      document.getElementById('log_scroll_control').querySelector('img').src = "../static/imgs/svg_icons/scroll_pause.svg";
    } else {
      document.getElementById('log_scroll_control').querySelector('img').src = "../static/imgs/svg_icons/scroll_down.svg";

    }
  }
  const scrollLogDown = () => {
    if(log_main.scrollHeight > log_main.clientHeight) { document.getElementById('log_scroll_control').style.display = 'initial'; }
    if(!scroll_paused) { log_main.scrollTop = log_main.scrollHeight; }
  }

</script>