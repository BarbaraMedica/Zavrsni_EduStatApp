<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >
    <div class="flex">

      <Sidebar :darkMode="darkMode" />

      <main class="flex-1 p-8">

        <!-- HEADER -->

        <div class="flex justify-between items-center mb-8">

          <div>

            <h1 class="text-4xl font-bold text-sky-700">

              🧠 AI analiza učenja

            </h1>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-2"
            >

              Personalizirana analiza studentskih navika učenja

            </p>

          </div>

          <button

            @click="generateDailyAnalysis"

            :disabled="loading"

            class="bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 rounded-xl shadow"

          >

            {{ loading ? "Analiziram..." : "🔄 Generiraj novu AI analizu" }}

          </button>

        </div>



        <!-- AI STATUS -->

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">

          <div
            class="rounded-2xl bg-gradient-to-br from-sky-500 to-blue-600
                   text-white p-6 shadow-lg"
          >

            <p class="text-sm opacity-80">

              Trenutno vrijeme

            </p>

            <h2 class="text-3xl font-bold mt-3">

              {{ currentTime }}

            </h2>

            <p class="mt-2 opacity-80">

              {{ currentDate }}

            </p>

          </div>



          <div
            :class="darkMode
              ? 'bg-slate-800'
              : 'bg-white'"
            class="rounded-2xl p-6 shadow-lg"
          >

            <p class="text-slate-500">

              Najbolje vrijeme

            </p>

            <h2 class="text-2xl font-bold text-sky-600 mt-2">

              {{ bestTime }}

            </h2>

            <p class="mt-3 text-sm text-slate-500">

              prema AI analizi

            </p>

          </div>



          <div
            :class="darkMode
              ? 'bg-slate-800'
              : 'bg-white'"
            class="rounded-2xl p-6 shadow-lg"
          >

            <p class="text-slate-500">

              Preporučeni predmet

            </p>

            <h2 class="text-2xl font-bold text-sky-600 mt-2">

              {{ recommendedSubject }}

            </h2>

            <p class="mt-3 text-sm text-slate-500">

              najveća očekivana produktivnost

            </p>

          </div>



          <div
            :class="darkMode
              ? 'bg-slate-800'
              : 'bg-white'"
            class="rounded-2xl p-6 shadow-lg"
          >

            <p class="text-slate-500">

              AI procjena

            </p>

            <h2
              class="text-2xl font-bold mt-2"
              :class="predictionColor"
            >

              {{ prediction }}

            </h2>

            <p class="mt-3 text-sm text-slate-500">

              {{ probability }} %

            </p>

          </div>

        </div>



        <!-- AI PREPORUKA -->

        <div
          :class="darkMode
            ? 'bg-slate-800'
            : 'bg-white'"
          class="rounded-2xl shadow-lg p-8 mb-8"
        >

          <div class="flex items-center gap-3 mb-6">

            <div
              class="w-12 h-12 rounded-full bg-sky-500
                     flex items-center justify-center text-white text-xl"
            >

              🤖

            </div>

            <div>

              <h2 class="text-2xl font-bold">

                AI preporuka za danas

              </h2>

              <p
                :class="darkMode
                  ? 'text-slate-400'
                  : 'text-slate-500'"
              >

                Generirano na temelju prethodnih analiza i
                Random Forest modela.

              </p>

            </div>

          </div>

          <div
            class="rounded-xl bg-sky-50 border border-sky-200
                   p-6 whitespace-pre-line leading-8"
            :class="darkMode
              ? 'bg-slate-700 border-slate-600'
              : ''"
          >

            {{ aiAdvice }}

          </div>

        </div>



        <!-- TIMELINE -->

        <div
          :class="darkMode
            ? 'bg-slate-800'
            : 'bg-white'"
          class="rounded-2xl shadow-lg p-8 mb-8"
        >

          <h2 class="text-2xl font-bold mb-6">

            📈 Preporučena produktivnost tijekom dana

          </h2>

          <div
            v-for="slot in timeline"
            :key="slot.hour"
            class="mb-5"
          >

            <div class="flex justify-between mb-2">

              <span class="font-medium">

                {{ slot.hour }}

              </span>

              <span class="text-slate-500">

                {{ slot.label }}

              </span>

            </div>

            <div
              class="w-full h-4 rounded-full overflow-hidden bg-slate-200"
            >

              <div

                class="h-4 bg-sky-500 rounded-full"

                :style="{

                  width: slot.score + '%'

                }"

              ></div>

            </div>

          </div>

        </div>



        <!-- POVIJEST -->

        <div
          :class="darkMode
            ? 'bg-slate-800'
            : 'bg-white'"
          class="rounded-2xl shadow-lg p-8"
        >

          <div class="flex justify-between items-center mb-6">

            <h2 class="text-2xl font-bold">

              📚 Povijest AI analiza

            </h2>

            <span class="text-slate-500">

              {{ analyses.length }} analiza

            </span>

          </div>

          <div
            v-if="analyses.length===0"
            class="text-center py-12 text-slate-500"
          >

            Još nema spremljenih analiza.

          </div>

          <div
            v-else
            class="space-y-5"
          >

            <div

              v-for="analysis in analyses"

              :key="analysis._id"

              class="rounded-xl border border-sky-100
                     bg-sky-50 p-5"

              :class="darkMode
                ? 'bg-slate-700 border-slate-600'
                : ''"

            >

              <div class="flex justify-between items-center">

                <div>

                  <h3 class="font-bold text-lg">

                    {{ analysis.subject }}

                  </h3>

                  <p class="text-sm text-slate-500">

                    {{ analysis.date }}

                  </p>

                </div>

                <span
                  class="bg-sky-500 text-white
                         px-4 py-1 rounded-full text-sm"
                >

                  AI analiza

                </span>

              </div>

              <p
                class="mt-5 whitespace-pre-line leading-7"
              >

                {{ analysis.text }}

              </p>

            </div>

          </div>

        </div>

      </main>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue"
import axios from "axios"
import Sidebar from "../components/Sidebar.vue"

const darkMode = ref(false)

const loading = ref(false)

const analyses = ref([])

const prediction = ref("-")
const probability = ref(0)

const aiAdvice = ref(
  "Kliknite na 'Generiraj novu AI analizu' kako bi aplikacija analizirala vaše dosadašnje navike."
)

const bestTime = ref("-")
const recommendedSubject = ref("-")

const currentTime = ref("")
const currentDate = ref("")

const api = "http://127.0.0.1:5000"

const predictionColor = computed(() => {

  if (prediction.value.includes("Dobro"))
    return "text-green-600"

  if (prediction.value.includes("Nije"))
    return "text-red-600"

  return "text-sky-600"

})

const timeline = ref([
  {
    hour:"06:00",
    score:20,
    label:"Niska produktivnost"
  },
  {
    hour:"08:00",
    score:55,
    label:"Dobra produktivnost"
  },
  {
    hour:"10:00",
    score:80,
    label:"Vrlo dobro"
  },
  {
    hour:"12:00",
    score:95,
    label:"Najbolje vrijeme"
  },
  {
    hour:"14:00",
    score:70,
    label:"Dobro"
  },
  {
    hour:"16:00",
    score:90,
    label:"Preporučeno"
  },
  {
    hour:"18:00",
    score:75,
    label:"Dobro"
  },
  {
    hour:"20:00",
    score:45,
    label:"Pad fokusa"
  },
  {
    hour:"22:00",
    score:15,
    label:"Nije preporučljivo"
  }
])

function updateClock(){

  const now = new Date()

  currentTime.value =
    now.toLocaleTimeString(
      "hr-HR",
      {
        hour:"2-digit",
        minute:"2-digit"
      }
    )

  currentDate.value =
    now.toLocaleDateString(
      "hr-HR",
      {
        weekday:"long",
        day:"numeric",
        month:"long",
        year:"numeric"
      }
    )

}
let timer = null

async function loadHistory() {

  try {

    const response = await axios.get(
      `${api}/analyses`
    )

    analyses.value = response.data

  }

  catch(error){

    console.error(error)

  }

}

async function generateDailyAnalysis(){

  loading.value = true

  try{

    const now = new Date()

    const response = await axios.post(

      `${api}/daily-analysis`,

      {

        current_hour: now.getHours(),

        current_date: now.toISOString()

      }

    )

    prediction.value =
      response.data.prediction

    probability.value =
      response.data.probability

    aiAdvice.value =
      response.data.ai_analysis

    bestTime.value =
      response.data.best_time

    recommendedSubject.value =
      response.data.subject

    if(response.data.timeline){

      timeline.value =
        response.data.timeline

    }

    await loadHistory()

  }

  catch(error){

    console.error(error)

    aiAdvice.value =
      "AI analiza trenutno nije dostupna."

  }

  finally{

    loading.value = false

  }

}

onMounted(()=>{

  updateClock()

  timer = setInterval(

    updateClock,

    60000

  )

  loadHistory()

  generateDailyAnalysis()

})

onBeforeUnmount(()=>{

  clearInterval(timer)

})
</script>

<style scoped>

::-webkit-scrollbar{

  width:8px;

}

::-webkit-scrollbar-thumb{

  background:#38bdf8;

  border-radius:20px;

}

::-webkit-scrollbar-track{

  background:transparent;

}

</style>