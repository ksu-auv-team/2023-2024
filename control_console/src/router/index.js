import { createRouter, createWebHistory } from 'vue-router';
import streamView from '@/views/streamView.vue';
import dataView from "@/views/dataView.vue";
import logView from "@/views/logView.vue";

const routes = [
  {
    path: '/',
    name: 'AUV Stream',
    component: streamView
  },
  {
    path: '/data',
    name: 'AUV Data',
    component: dataView
  },
  {
    path: '/log',
    name: 'AUV Log',
    component: logView
  },
  // Error route - page not found
  {
    path: '/:pathMatch(.*)*',
    name: 'AUV Stream',
    component: streamView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
