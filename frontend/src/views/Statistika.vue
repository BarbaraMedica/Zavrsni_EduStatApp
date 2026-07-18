<template>
  <div class="card">
    <h2>Statistika učenja</h2>

    <p>Broj analiza: {{ history.length }}</p>
    <p>Prosječni fokus: {{ avgFocus }}</p>
    <p>Prosječni stres: {{ avgStress }}</p>

    <canvas id="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const history = ref([])

const avgFocus = ref(0)
const avgStress = ref(0)

onMounted(() => {
  history.value = JSON.parse(localStorage.getItem("history")) || []

  if (history.value.length > 0) {
    avgFocus.value = (
      history.value.reduce((a, b) => a + b.focus, 0) /
      history.value.length
    ).toFixed(1)

    avgStress.value = (
      history.value.reduce((a, b) => a + b.stress, 0) /
      history.value.length
    ).toFixed(1)
  }

  renderChart()
})

function renderChart() {
  const ctx = document.getElementById("chart")

  new Chart(ctx, {
    type: "line",
    data: {
      labels: history.value.map((_, i) => `Unos ${i + 1}`),

      datasets: [
        {
          label: "Fokus",
          data: history.value.map(h => h.focus),
          borderColor: "blue"
        },
        {
          label: "Stres",
          data: history.value.map(h => h.stress),
          borderColor: "red"
        },
        {
          label: "Energija",
          data: history.value.map(h => h.energy),
          borderColor: "green"
        }
      ]
    }
  })
}
</script>

<style>
.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}
</style>