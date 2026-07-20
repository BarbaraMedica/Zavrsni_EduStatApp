<template>
  <div class="min-h-screen bg-gradient-to-br from-sky-100 via-sky-200 to-sky-300 text-slate-900">
    <div class="flex">
      <Sidebar :darkMode="false" />

      <main class="flex-1 p-8">
        <div class="max-w-4xl mx-auto">
          <div class="mb-8 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h1 class="text-4xl font-bold text-sky-700">Postavke</h1>
              <p class="text-slate-600 mt-2">Podešavanja izgleda i ponašanja za završni rad.</p>
            </div>
            <button class="rounded-2xl bg-sky-600 px-5 py-3 text-white shadow-lg hover:bg-sky-700 transition">Spremi postavke</button>
          </div>

          <div class="grid gap-6">
            <div class="rounded-3xl bg-sky-50 border border-sky-100 p-6 shadow-sm">
              <h2 class="text-xl font-semibold text-sky-700 mb-3">Tema</h2>
              <p class="text-slate-600 mb-4">Aplikacija koristi plavu paletu boja i svijetlo plave prozore.</p>
              <div class="space-y-4">
                <label class="flex items-center gap-3 rounded-2xl bg-white p-4 border border-slate-200 shadow-sm">
                  <input type="radio" name="theme" checked />
                  <span>Plava tema</span>
                </label>
                <label class="flex items-center gap-3 rounded-2xl bg-white p-4 border border-slate-200 shadow-sm">
                  <input type="radio" name="theme" disabled />
                  <span>Svijetlo plava (preporučeno)</span>
                </label>
              </div>
            </div>

            <div class="rounded-3xl bg-sky-50 border border-sky-100 p-6 shadow-sm">
              <h2 class="text-xl font-semibold text-sky-700 mb-3">O aplikaciji</h2>
              <p class="text-slate-600">Ovaj projekt služi kao završni rad i uključuje analize učenja, bilješke, predmete i statistiku u realnom vremenu preko Flask backenda i MongoDB baze.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(false)
</script>

<style scoped>
button[type="button"] {
  border-radius: 1rem;
}
</style>
