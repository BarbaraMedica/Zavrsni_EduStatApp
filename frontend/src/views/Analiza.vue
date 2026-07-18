<template>
  <div class="min-h-screen bg-sky-50 flex justify-center p-6">

    <div class="w-full max-w-3xl bg-white rounded-2xl shadow-sm border border-sky-100 p-6">

    <h2 class="text-2xl font-semibold text-sky-700 mb-6">Analiza učenja</h2>

    <div class="grid grid-cols-2 gap-4">
      <input v-model="form.sleep_hours" type="number" placeholder="Sati sna" />
      <input v-model="form.study_duration" type="number" placeholder="Trajanje učenja (min)" />
      <input v-model="form.breaks" type="number" placeholder="Broj pauza" />
      <input v-model="form.time_of_day" type="number" placeholder="Vrijeme (0-23)" />
      <input v-model="form.focus" type="number" placeholder="Fokus (1-10)" />
      <input v-model="form.stress" type="number" placeholder="Stres (1-10)" />
      <input v-model="form.energy" type="number" placeholder="Energija (1-10)" />
    </div>

    <button class="btn" @click="predict">Analiziraj</button>

    <div v-if="result" class="mt-6 p-4 rounded-xl bg-sky-50 border border-sky-100" :class="resultClass">
      <h3>{{ result }}</h3>
      <p class="text-slate-500">Vjerojatnost: {{ probability }}</p>
      <p class="mt-2 text-slate-600">{{ advice }}</p>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  sleep_hours: 7,
  study_duration: 90,
  breaks: 2,
  time_of_day: 14,
  focus: 7,
  stress: 4,
  energy: 8
})

const result = ref('')
const probability = ref('')
const advice = ref('')
const resultClass = ref('')

const predict = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:5000/predict', form.value)

    result.value = res.data.rezultat
    probability.value = res.data.vjerojatnost

    if (result.value.includes("Dobro")) {
      resultClass.value = "good"
    } else {
      resultClass.value = "bad"
    }

    generateAdvice()

  } catch (err) {
    alert("Greška pri pozivu backenda")
  }
}

function generateAdvice() {
  if (form.value.sleep_hours < 6) {
    advice.value = "Premalo sna smanjuje fokus. Pokušaj spavati barem 7h."
  } else if (form.value.stress > 7) {
    advice.value = "Visok stres - preporučuje se pauza prije učenja."
  } else if (form.value.study_duration > 120) {
    advice.value = "Dugo učiš - napravi kratku pauzu."
  } else {
    advice.value = "Nastavi s dobrim navikama!"
  }
}
</script>

<style>
.card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  background: #4f46e5;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
}

.good {
  background: #dcfce7;
  color: #166534;
}

.bad {
  background: #fee2e2;
  color: #991b1b;
}
</style>