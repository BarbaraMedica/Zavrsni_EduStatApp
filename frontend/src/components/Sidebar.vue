<template>
  <aside :class="sidebarClass" class="w-72 min-h-screen border-r p-5 hidden lg:block">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-sky-600">StudyAI</h1>
      <p :class="descriptionClass" class="text-sm mt-1">AI analiza studentskih navika</p>
    </div>

    <div class="space-y-2">
      <router-link
        v-for="item in links"
        :key="item.path"
        :to="item.path"
        class="block p-3 rounded-xl transition cursor-pointer"
        :class="linkClass(item.path)"
      >
        <span class="mr-2">{{ item.icon }}</span>
        {{ item.label }}
      </router-link>
    </div>

    <div :class="cardClass" class="mt-10 rounded-2xl p-5">
      <p class="text-sm text-slate-500">AI Score</p>
      <h2 class="text-4xl font-bold text-sky-600 mt-2">82</h2>
      <p class="text-sm text-emerald-500 mt-2">Produktivnost raste 📈</p>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  darkMode: {
    type: Boolean,
    default: false
  }
})

const route = useRoute()

const links = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/analiza', label: 'AI analiza', icon: '🧠' },
  { path: '/zapisivanje', label: 'Zapisivanje', icon: '✍️' },
  { path: '/biljeske', label: 'Bilješke', icon: '📝' },
  { path: '/statistika', label: 'Statistika', icon: '📈' },
  { path: '/predmeti', label: 'Predmeti', icon: '📚' },
  { path: '/postavke', label: 'Postavke', icon: '⚙️' }
]

const sidebarClass = computed(() =>
  props.darkMode
    ? 'bg-slate-800 border-slate-700 text-white'
    : 'bg-white border-sky-100 text-slate-800'
)

const cardClass = computed(() =>
  props.darkMode
    ? 'bg-slate-700 text-white'
    : 'bg-sky-50 border border-sky-100 text-slate-800'
)

const descriptionClass = computed(() =>
  props.darkMode ? 'text-slate-400' : 'text-slate-500'
)

const linkClass = path =>
  route.path === path
    ? 'bg-sky-100 text-sky-700 font-medium'
    : props.darkMode
      ? 'hover:bg-slate-700 text-slate-200'
      : 'hover:bg-sky-50 text-slate-600'
</script>
