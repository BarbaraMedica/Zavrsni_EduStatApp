import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Analiza from '../views/Analiza.vue'
import Statistika from '../views/Statistika.vue'
import Biljeske from '../views/Biljeske.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/analiza', component: Analiza },
  { path: '/statistika', component: Statistika },
  { path: '/biljeske', component: Biljeske }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router