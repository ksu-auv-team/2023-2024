import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';

import '@/assets/style.css';
// import '@/assets/js/charts';
// import '@/assets/js/index';


createApp(App).use(router).use(store).mount('#app')
