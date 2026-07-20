import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Analiza from '../views/Analiza.vue'
import Statistika from '../views/Statistika.vue'
import Biljeske from '../views/Biljeske.vue'
import Zapisivanje from '../views/Zapisivanje.vue'
import Predmeti from '../views/Predmeti.vue'
import Postavke from '../views/Postavke.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/analiza', component: Analiza },
  { path: '/statistika', component: Statistika },
  { path: '/biljeske', component: Biljeske },
  { path: '/zapisivanje', component: Zapisivanje },
  { path: '/predmeti', component: Predmeti },
  { path: '/postavke', component: Postavke }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router