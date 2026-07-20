<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >
    <div class="flex">
      <Sidebar :darkMode="darkMode" />

      <!-- MAIN -->
      <main class="flex-1 p-6">

        <!-- HEADER -->
        <div class="flex justify-between items-center mb-8">

          <div>
            <h1 class="text-3xl font-bold text-sky-700">
              Pozdrav, Barbara 👋
            </h1>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-1"
            >
              Pregled studentskih navika učenja
            </p>
          </div>

          <!-- DARK MODE -->
          <button
            @click="darkMode = !darkMode"
            class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-xl transition"
          >
            {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
          </button>

        </div>

        <!-- STATS -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">

          <!-- CARD -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">
              Vrijeme učenja
            </p>

            <h2 class="text-3xl font-bold text-sky-600 mt-2">
              {{ totalHours }}h
            </h2>

            <p class="text-xs text-slate-400 mt-1">
              ovaj tjedan
            </p>
          </div>

          <!-- CARD -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">
              Produktivnost
            </p>

            <h2 class="text-3xl font-bold text-sky-600 mt-2">
              {{ avgProductivity }}
            </h2>

            <p class="text-xs text-slate-400 mt-1">
              /10
            </p>
          </div>

          <!-- CARD -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">
              Fokus
            </p>

            <h2 class="text-3xl font-bold text-sky-600 mt-2">
              {{ avgFocus }}
            </h2>

            <p class="text-xs text-slate-400 mt-1">
              /10
            </p>
          </div>

          <!-- CARD -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">
              Stres
            </p>

            <h2 class="text-3xl font-bold text-sky-600 mt-2">
              {{ avgStress }}
            </h2>

            <p class="text-xs text-slate-400 mt-1">
              /10
            </p>
          </div>

        </div>

        <!-- MAIN CONTENT -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

          <!-- AI ANALIZA -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="lg:col-span-2 rounded-2xl border p-6 shadow-sm"
          >

            <div class="flex justify-between items-center mb-4">

              <h2 class="text-xl font-semibold text-sky-700">
                🧠 AI analiza
              </h2>

              <button
                class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-xl transition"
              >
                Osvježi AI
              </button>

            </div>

            <div class="space-y-5">

              <div>
                <h3 class="font-semibold mb-2">
                  Interpretacija:
                </h3>

                <p
                  :class="darkMode ? 'text-slate-300' : 'text-slate-600'"
                >
                  Primjećuje se da student postiže najbolje rezultate
                  tijekom jutarnjih sati kada je razina energije viša,
                  a stres niži.
                </p>
              </div>

              <div>
                <h3 class="font-semibold mb-2">
                  AI savjet:
                </h3>

                <p class="text-sky-600">
                  Preporučuje se učenje u kraćim intervalima
                  od 45 do 60 minuta uz redovite pauze.
                </p>
              </div>

              <div>
                <h3 class="font-semibold mb-2">
                  Preporučene akcije:
                </h3>

                <ul
                  :class="darkMode ? 'text-slate-300' : 'text-slate-600'"
                  class="space-y-2 text-sm"
                >
                  <li>• Koristiti jutarnje termine za teže predmete</li>
                  <li>• Izbjegavati učenje nakon 22h</li>
                  <li>• Povećati broj kratkih pauza</li>
                </ul>
              </div>

            </div>

          </div>

          <!-- RECENT -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >

            <h2 class="text-xl font-semibold text-sky-700 mb-4">
              📚 Zadnje sesije
            </h2>

            <div class="space-y-3">

              <div
                v-for="(l, i) in logs.slice(0,5)"
                :key="i"
                :class="darkMode
                  ? 'bg-slate-700'
                  : 'bg-sky-50 border border-sky-100'"
                class="p-3 rounded-xl"
              >

                <p class="font-medium">
                  {{ l.subject || 'Nema predmeta' }}
                </p>

                <p class="text-sm text-slate-500 mt-1">
                  Fokus: {{ l.focus }} |
                  Stres: {{ l.stress }}
                </p>

              </div>

            </div>

          </div>

        </div>

        <!-- WEEKLY -->
        <div
          :class="darkMode
            ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mt-6"
        >

          <h2 class="text-xl font-semibold text-sky-700 mb-5">
            📈 Tjedni pregled
          </h2>

          <div class="space-y-4">

            <div
              v-for="d in chartData"
              :key="d.day"
            >

              <div class="flex justify-between text-sm mb-1">

                <span>
                  {{ d.day }}
                </span>

                <span class="text-slate-500">
                  Fokus {{ d.productivity }} / Stres {{ d.stress }}
                </span>

              </div>

              <div class="w-full bg-slate-200 rounded-full h-3 overflow-hidden">

                <div
                  class="bg-sky-500 h-3 rounded-full"
                  :style="{ width: (d.productivity * 10) + '%' }"
                ></div>

              </div>

            </div>

          </div>

        </div>

      </main>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(false)
const logs = ref([])
const apiBase = 'http://127.0.0.1:5000'

const loadStatistics = async () => {
  try {
    const response = await axios.get(`${apiBase}/statistics`)
    logs.value = response.data.history || []
  } catch (error) {
    console.error('Greška pri dohvaćanju statistike', error)
    alert('Greška pri učitavanju statistike.')
  }
}

onMounted(() => {
  loadStatistics()
})

const totalHours = computed(() =>
  (
    logs.value.reduce(
      (s, l) => s + Number(l.study_duration || 0),
      0
    ) / 60
  ).toFixed(1)
)

const avgProductivity = computed(() =>
  logs.value.length
    ? (
        logs.value.reduce(
          (s, l) => s + Number(l.probability || 0),
          0
        ) / logs.value.length * 10
      ).toFixed(1)
    : 0
)

const avgFocus = computed(() =>
  logs.value.length
    ? (
        logs.value.reduce(
          (s, l) => s + Number(l.focus || 0),
          0
        ) / logs.value.length
      ).toFixed(1)
    : 0
)

const avgStress = computed(() =>
  logs.value.length
    ? (
        logs.value.reduce(
          (s, l) => s + Number(l.stress || 0),
          0
        ) / logs.value.length
      ).toFixed(1)
    : 0
)

const chartData = computed(() => {
  const days = [
    'Pon',
    'Uto',
    'Sri',
    'Čet',
    'Pet',
    'Sub',
    'Ned'
  ]

  return days.map((day, i) => {
    const entry = logs.value[i] || {}

    return {
      day,
      productivity: entry.probability ? Number(entry.probability) * 10 : 0,
      stress: entry.stress || 0
    }
  })
})
</script>

<style>

</style>