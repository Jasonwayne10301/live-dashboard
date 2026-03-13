import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const routes = [
  { path: '/', component: DashboardView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
