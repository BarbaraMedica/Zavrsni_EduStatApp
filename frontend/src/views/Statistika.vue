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
              Statistika učenja 📈
            </h1>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-1"
            >
              Pregled AI analiza spremljenih u MongoDB bazu.
            </p>
          </div>

          <button
            @click="darkMode=!darkMode"
            class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-xl transition"
          >
            {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
          </button>

        </div>

        <!-- INFO KARTICE -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >

            <p class="text-sm text-slate-500">
              Ukupno analiza
            </p>

            <h2 class="text-4xl font-bold text-sky-600 mt-2">
              {{ total }}
            </h2>

          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >

            <p class="text-sm text-slate-500">
              Prosječni fokus
            </p>

            <h2 class="text-4xl font-bold text-emerald-600 mt-2">
              {{ avgFocus }}/10
            </h2>

          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >

            <p class="text-sm text-slate-500">
              Prosječni stres
            </p>

            <h2 class="text-4xl font-bold text-rose-500 mt-2">
              {{ avgStress }}/10
            </h2>

          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >

            <p class="text-sm text-slate-500">
              Prosječna energija
            </p>

            <h2 class="text-4xl font-bold text-amber-500 mt-2">
              {{ avgEnergy }}/10
            </h2>

          </div>

        </div>

        <!-- GRAF -->
        <div
          :class="darkMode ? 'bg-slate-800 border-slate-700'
          : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mb-8"
        >

          <div class="flex justify-between items-center mb-6">

            <h2 class="text-xl font-semibold text-sky-700">
              Trend AI analiza
            </h2>

            <span class="text-sm text-slate-500">
              Fokus • Stres • Energija
            </span>

          </div>

          <canvas id="chart" height="100"></canvas>

        </div>

        <!-- TABLICA -->
        <div
          :class="darkMode ? 'bg-slate-800 border-slate-700'
          : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm"
        >

          <div class="flex justify-between items-center mb-6">

            <h2 class="text-xl font-semibold text-sky-700">
              Posljednje AI analize
            </h2>

            <span class="text-sm text-slate-500">
              {{ history.length }} zapisa
            </span>

          </div>

          <div
            v-if="history.length===0"
            class="text-center py-10 text-slate-400"
          >
            Nema spremljenih analiza.
          </div>

          <div
            v-else
            class="overflow-x-auto"
          >

            <table class="w-full">

              <thead>

                <tr
                  class="border-b"
                >

                  <th class="text-left py-3">
                    #
                  </th>

                  <th class="text-left py-3">
                    Fokus
                  </th>

                  <th class="text-left py-3">
                    Stres
                  </th>

                  <th class="text-left py-3">
                    Energija
                  </th>

                  <th class="text-left py-3">
                    Rezultat
                  </th>

                  <th class="text-left py-3">
                    Vjerojatnost
                  </th>

                </tr>

              </thead>

              <tbody>

                <tr
                  v-for="(item,index) in history"
                  :key="index"
                  class="border-b hover:bg-sky-50 transition"
                >

                  <td class="py-3">
                    {{ index+1 }}
                  </td>

                  <td class="py-3">
                    {{ item.focus }}
                  </td>

                  <td class="py-3">
                    {{ item.stress }}
                  </td>

                  <td class="py-3">
                    {{ item.energy }}
                  </td>

                  <td class="py-3">

                    <span
                      :class="item.result.includes('Dobro')
                      ? 'text-emerald-600'
                      : 'text-rose-500'"
                      class="font-semibold"
                    >
                      {{ item.result }}
                    </span>

                  </td>

                  <td class="py-3">
                    {{ item.probability }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </div>

      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(false)

const total = ref(0)
const avgFocus = ref(0)
const avgStress = ref(0)
const avgEnergy = ref(0)

const history = ref([])

let chart = null

async function loadStatistics() {

  try {

    const response = await axios.get(
      "http://127.0.0.1:5000/statistics"
    )

    total.value = response.data.total
    avgFocus.value = response.data.avg_focus
    avgStress.value = response.data.avg_stress
    avgEnergy.value = response.data.avg_energy

    history.value = response.data.history

    renderChart()

  }

  catch (error) {

    console.error(error)

    alert("Greška pri dohvaćanju statistike.")

  }

}

function renderChart() {

  if (history.value.length === 0)
    return

  const ctx = document.getElementById("chart")

  if (chart)
    chart.destroy()

  chart = new Chart(ctx, {

    type: "line",

    data: {

      labels: history.value.map(
        (_, index) => `Analiza ${index + 1}`
      ),

      datasets: [

        {

          label: "Fokus",

          data: history.value.map(
            item => item.focus
          ),

          borderColor: "#0ea5e9",

          backgroundColor: "#0ea5e9",

          tension: 0.3

        },

        {

          label: "Stres",

          data: history.value.map(
            item => item.stress
          ),

          borderColor: "#ef4444",

          backgroundColor: "#ef4444",

          tension: 0.3

        },

        {

          label: "Energija",

          data: history.value.map(
            item => item.energy
          ),

          borderColor: "#10b981",

          backgroundColor: "#10b981",

          tension: 0.3

        }

      ]

    },

    options: {

      responsive: true,

      maintainAspectRatio: true,

      plugins: {

        legend: {

          position: "top"

        }

      },

      scales: {

        y: {

          beginAtZero: true,

          max: 10

        }

      }

    }

  })

}

onMounted(() => {

  loadStatistics()

})

</script>

<style scoped>

table {

  border-collapse: collapse;

}

th {

  font-weight: 600;

}

canvas {

  max-height: 350px;

}

</style>
