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
              Zapisivanje učenja ✍️
            </h1>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-1"
            >
              Unesi podatke za AI analizu studentskih navika
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

        <!-- MAIN GRID -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

          <!-- FORM -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="lg:col-span-2 rounded-2xl border p-6 shadow-sm"
          >

            <!-- DATE + SUBJECT -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">

              <div>
                <label class="text-sm text-slate-500">
                  Datum
                </label>

                <input
                  type="date"
                  v-model="form.date"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

              <div>
                <label class="text-sm text-slate-500">
                  Predmet
                </label>

                <input
                  type="text"
                  v-model="form.subject"
                  placeholder="npr. Matematika"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

            </div>

            <!-- TIME + DURATION -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">

              <div>
                <label class="text-sm text-slate-500">
                  Vrijeme dana
                </label>

                <select
                  v-model="form.time_of_day"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                >
                  <option value="0">🌅 Jutro</option>
                  <option value="1">☀️ Podne</option>
                  <option value="2">🌤 Popodne</option>
                  <option value="3">🌙 Večer</option>
                </select>
              </div>

              <div>
                <label class="text-sm text-slate-500">
                  Trajanje učenja (min)
                </label>

                <input
                  type="number"
                  v-model="form.study_duration"
                  placeholder="npr. 90"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

            </div>

            <!-- EXTRA -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">

              <div>
                <label class="text-sm text-slate-500">
                  San (h)
                </label>

                <input
                  type="number"
                  v-model="form.sleep_hours"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

              <div>
                <label class="text-sm text-slate-500">
                  Pauze
                </label>

                <input
                  type="number"
                  v-model="form.breaks"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

              <div>
                <label class="text-sm text-slate-500">
                  Energija
                </label>

                <input
                  type="number"
                  v-model="form.energy"
                  :class="darkMode
                    ? 'bg-slate-700 border-slate-600 text-white'
                    : 'bg-sky-50 border-sky-100'"
                  class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
                />
              </div>

            </div>

            <!-- SLIDERS -->
            <div class="space-y-6 mb-6">

              <!-- FOCUS -->
              <div>
                <div class="flex justify-between mb-2">
                  <span class="font-medium">
                    🧠 Fokus
                  </span>

                  <span class="text-sky-600 font-semibold">
                    {{ form.focus }}/10
                  </span>
                </div>

                <input
                  type="range"
                  min="1"
                  max="10"
                  v-model="form.focus"
                  class="w-full accent-sky-500"
                />
              </div>

              <!-- STRESS -->
              <div>
                <div class="flex justify-between mb-2">
                  <span class="font-medium">
                    😵 Stres
                  </span>

                  <span class="text-rose-500 font-semibold">
                    {{ form.stress }}/10
                  </span>
                </div>

                <input
                  type="range"
                  min="1"
                  max="10"
                  v-model="form.stress"
                  class="w-full accent-rose-400"
                />
              </div>

              <!-- ENERGY -->
              <div>
                <div class="flex justify-between mb-2">
                  <span class="font-medium">
                    ⚡ Energija
                  </span>

                  <span class="text-emerald-500 font-semibold">
                    {{ form.energy }}/10
                  </span>
                </div>

                <input
                  type="range"
                  min="1"
                  max="10"
                  v-model="form.energy"
                  class="w-full accent-emerald-500"
                />
              </div>

            </div>

            <!-- NOTES -->
            <div class="mb-6">

              <label class="text-sm text-slate-500">
                Bilješke
              </label>

              <textarea
                v-model="form.notes"
                placeholder="Kako je prošlo učenje?"
                :class="darkMode
                  ? 'bg-slate-700 border-slate-600 text-white'
                  : 'bg-sky-50 border-sky-100'"
                class="w-full mt-2 p-4 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none h-28 resize-none"
              ></textarea>

            </div>

            <!-- BUTTON -->
            <button
              @click="save"
              class="w-full bg-sky-500 hover:bg-sky-600 text-white py-4 rounded-xl font-semibold transition shadow-md"
            >
              Spremi AI analizu
            </button>

          </div>

          <!-- AI RESULT -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm h-fit"
          >

            <h2 class="text-xl font-semibold text-sky-700 mb-5">
              🧠 AI Procjena
            </h2>

            <div class="space-y-5">

              <div>
                <p class="text-sm text-slate-500 mb-2">
                  Predikcija produktivnosti
                </p>

                <div class="text-3xl font-bold text-sky-600">
                  {{ result ? result.prediction : 'Čeka analizu...' }}
                </div>
              </div>

              <div class="bg-sky-50 rounded-2xl p-4 border border-sky-100">
                <h3 class="font-semibold text-sky-700 mb-2">
                  AI Insight
                </h3>

                <p class="text-sm text-slate-600 leading-relaxed">
                  {{ result ? result.ai_analysis : 'Nakon spremanja podataka, ovdje će se pojaviti AI analiza.' }}
                </p>
              </div>

              <div class="bg-emerald-50 rounded-2xl p-4 border border-emerald-100">
                <h3 class="font-semibold text-emerald-700 mb-2">
                  Vjerojatnost
                </h3>

                <p class="text-sm text-slate-600 leading-relaxed">
                  {{ result ? `${result.probability}%` : '—' }}
                </p>
              </div>

            </div>

          </div>

        </div>

      </main>

    </div>

  </div>
</template>

<script setup>

import { ref } from 'vue'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(false)



const result = ref(null)



const form = ref({

  date: new Date()
    .toISOString()
    .split('T')[0],


  subject:'',

  study_duration:'',

  time_of_day:0,

  focus:5,

  stress:5,

  energy:5,

  sleep_hours:7,

  breaks:2,

  notes:''

})





async function save() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/analyze', {
      date: form.value.date,
      subject: form.value.subject,
      sleep_hours: Number(form.value.sleep_hours),
      study_duration: Number(form.value.study_duration),
      breaks: Number(form.value.breaks),
      time_of_day: Number(form.value.time_of_day),
      focus: Number(form.value.focus),
      stress: Number(form.value.stress),
      energy: Number(form.value.energy),
      notes: form.value.notes
    })

    result.value = response.data
    alert('AI analiza spremljena u MongoDB')
  } catch (error) {
    console.error(error)
    alert('Greška kod povezivanja s backendom')
  }
}


</script>

<style>

</style>