<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >
    <div class="flex">
      <Sidebar :darkMode="darkMode" />

      <main class="flex-1 p-8">
        <div class="max-w-4xl mx-auto">
          <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h1
                class="text-4xl font-bold"
                :class="darkMode ? 'text-white' : 'text-sky-700'"
              >
                Postavke
              </h1>
              <p
                class="mt-2"
                :class="darkMode ? 'text-slate-400' : 'text-slate-600'"
              >
                Podešavanja izgleda i ponašanja aplikacije.
              </p>
            </div>

            <div class="flex items-center gap-3">
              <button
                @click="saveSettings"
                class="rounded-2xl bg-sky-600 px-5 py-3 text-white shadow-lg hover:bg-sky-700 transition"
              >
                Spremi postavke
              </button>

              <button
                @click="darkMode = !darkMode; localStorage.setItem('darkMode', String(darkMode))"
                class="bg-slate-700 hover:bg-slate-800 text-white px-4 py-2 rounded-xl transition"
              >
                {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
              </button>
            </div>
          </div>

          <div class="grid gap-6">
            <div
              class="rounded-3xl p-6 shadow-sm"
              :class="darkMode ? 'bg-slate-800 border border-slate-700' : 'bg-sky-50 border border-sky-100'"
            >
              <h2
                class="text-xl font-semibold mb-3"
                :class="darkMode ? 'text-white' : 'text-sky-700'"
              >
                Tema
              </h2>
              <p
                class="mb-4"
                :class="darkMode ? 'text-slate-400' : 'text-slate-600'"
              >
                Aplikacija koristi plavu paletu boja i svijetlo plave prozore.
              </p>
              <div class="space-y-4">
                <label
                  class="flex items-center gap-3 rounded-2xl p-4 border shadow-sm"
                  :class="darkMode ? 'bg-slate-700 border-slate-600 text-white' : 'bg-white border-slate-200 text-slate-800'"
                >
                  <input type="radio" name="theme" checked />
                  <span>Plava tema</span>
                </label>
                <label
                  class="flex items-center gap-3 rounded-2xl p-4 border shadow-sm"
                  :class="darkMode ? 'bg-slate-700 border-slate-600 text-white' : 'bg-white border-slate-200 text-slate-800'"
                >
                  <input type="radio" name="theme" disabled />
                  <span>Svijetlo plava (preporučeno)</span>
                </label>
              </div>
            </div>

            <div
              class="rounded-3xl p-6 shadow-sm"
              :class="darkMode ? 'bg-slate-800 border border-slate-700' : 'bg-sky-50 border border-sky-100'"
            >
              <h2
                class="text-xl font-semibold mb-3"
                :class="darkMode ? 'text-white' : 'text-sky-700'"
              >
                Korisnički profil
              </h2>

              <p
                class="mb-4"
                :class="darkMode ? 'text-slate-400' : 'text-slate-600'"
              >
                Unesite ime koje će se prikazivati na početnoj stranici.
              </p>

              <input
                v-model="username"
                type="text"
                placeholder="Unesite ime"
                :class="darkMode ? 'bg-slate-700 border-slate-600 text-white placeholder:text-slate-400' : 'border-slate-200 bg-white text-slate-800'"
                class="w-full rounded-2xl border px-4 py-3 outline-none focus:ring-2 focus:ring-sky-400"
              />
            </div>

            <div
              class="rounded-3xl p-6 shadow-sm"
              :class="darkMode ? 'bg-slate-800 border border-slate-700' : 'bg-sky-50 border border-sky-100'"
            >
              <h2
                class="text-xl font-semibold mb-3"
                :class="darkMode ? 'text-white' : 'text-sky-700'"
              >
                O aplikaciji
              </h2>
              <p :class="darkMode ? 'text-slate-400' : 'text-slate-600'">
                Ovaj projekt služi kao završni rad i uključuje analize učenja, bilješke, predmete i statistiku u realnom vremenu preko Flask backenda i MongoDB baze.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(localStorage.getItem('darkMode') === 'true')
const username = ref('')

onMounted(() => {
  const savedName = localStorage.getItem('username')

  if (savedName) {
    username.value = savedName
  }
})

function saveSettings() {
  localStorage.setItem('username', username.value)
  alert('Postavke spremljene!')
}
</script>
<style>
  button[type="button"] {
    border-radius: 1rem;
  }
</style>
