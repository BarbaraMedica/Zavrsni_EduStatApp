<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >
    <div class="flex">
      <Sidebar :darkMode="darkMode" />

      <main class="flex-1 p-6">

       <div class="flex justify-between items-center mb-8">

        <div>
          <h1 class="text-4xl font-bold text-sky-700">
            Pozdrav, {{ username }} 
          </h1>

          <p
            :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            class="mt-1"
          >
            Pregled studentskih navika učenja
          </p>
        </div>

        <div class="flex items-center gap-3">

          <button
            @click="refreshData"
            class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-xl transition"
          >
            🔄 Osvježi AI
          </button>

          <button
            @click="darkMode = !darkMode"
            class="bg-slate-700 hover:bg-slate-800 text-white px-4 py-2 rounded-xl transition"
          >
            {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
          </button>

        </div>

      </div>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">Vrijeme učenja</p>
            <h2 class="text-3xl font-bold text-sky-600 mt-2">{{ totalHours }}h</h2>
            <p class="text-xs text-slate-400 mt-1">ukupno</p>
          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">Produktivnost</p>
            <h2 class="text-3xl font-bold text-sky-600 mt-2">{{ avgProductivity }}%</h2>
            <p class="text-xs text-slate-400 mt-1">prosjek</p>
          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">Fokus</p>
            <h2 class="text-3xl font-bold text-sky-600 mt-2">{{ avgFocus }}</h2>
            <p class="text-xs text-slate-400 mt-1">/10</p>
          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="rounded-2xl border p-5 shadow-sm"
          >
            <p class="text-sm text-slate-500">Stres</p>
            <h2 class="text-3xl font-bold text-sky-600 mt-2">{{ avgStress }}</h2>
            <p class="text-xs text-slate-400 mt-1">/10</p>
          </div>
        </div>
        <!-- OPTIMALNI TRENUTAK ZA UČENJE -->
        <div
          :class="darkMode
            ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mb-6"
        >
          <div class="flex items-center justify-between mb-5">
            <div>
              <h2 class="text-xl font-semibold text-sky-700">
                🧠 Tvoj optimalni trenutak za učenje
              </h2>

              <p
                :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
                class="text-sm mt-1"
              >
                Prema tvojim dosadašnjim sesijama učenja
              </p>
            </div>

            <span class="text-3xl">🎯</span>
          </div>

          <div v-if="optimalData.hasData">

            <div class="grid grid-cols-2 md:grid-cols-5 gap-3">

              <div
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50'"
                class="rounded-xl p-4"
              >
                <p class="text-xs text-slate-500 mb-1">Najproduktivniji predmet</p>
                <p class="font-semibold">
                  📚 {{ optimalData.subject }}
                </p>
              </div>

              <div
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50'"
                class="rounded-xl p-4"
              >
                <p class="text-xs text-slate-500 mb-1">San</p>
                <p class="font-semibold">
                   {{ optimalData.sleep }} h
                </p>
              </div>

              <div
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50'"
                class="rounded-xl p-4"
              >
                <p class="text-xs text-slate-500 mb-1">Najbolje vrijeme</p>
                <p class="font-semibold">
                   {{ optimalData.time }}
                </p>
              </div>

              <div
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50'"
                class="rounded-xl p-4"
              >
                <p class="text-xs text-slate-500 mb-1">Trajanje</p>
                <p class="font-semibold">
                   {{ optimalData.duration }} min
                </p>
              </div>

              <div
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50'"
                class="rounded-xl p-4"
              >
                <p class="text-xs text-slate-500 mb-1">Prosječan fokus</p>
                <p class="font-semibold">
                   {{ optimalData.focus }}/10
                </p>
              </div>

            </div>

            <div
              :class="darkMode
                ? 'bg-slate-700/60 text-slate-300'
                : 'bg-sky-50 text-slate-600'"
              class="mt-4 rounded-xl p-4 text-sm leading-6"
            >
              💡 Prema tvojim dosadašnjim rezultatima, najbolje uvjete za učenje
              ostvaruješ uz približno
              <strong>{{ optimalData.sleep }} sati sna</strong>,
              tijekom
              <strong>{{ optimalData.time }}</strong>,
              uz sesiju od oko
              <strong>{{ optimalData.duration }} minuta</strong>.
            </div>

          </div>

          <div
            v-else
            :class="darkMode
              ? 'bg-slate-700 text-slate-300'
              : 'bg-sky-50 text-slate-500'"
            class="rounded-xl p-4 text-sm"
          >
            Dodaj nekoliko sesija učenja kako bi StudyAI mogao
            pronaći tvoje optimalne uvjete za učenje.
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="lg:col-span-2 rounded-2xl border p-6 shadow-sm"
          >
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold text-sky-700">🧠 AI analiza</h2>
            </div>

            <div class="space-y-5">
              <div>
                <h3 class="font-semibold text-lg mb-4">
                   Sažetak tvoje analize
                </h3>

                <div
                  :class="darkMode
                    ? 'bg-slate-700 text-slate-200'
                    : 'bg-sky-50 text-slate-700'"
                  class="rounded-xl p-5 whitespace-pre-line leading-7"
                >
                  {{ aiAnalysis || 'Nema dostupne AI analize.' }}
                </div>
              </div>
            </div>
          </div>

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm"
          >
            <h2 class="text-xl font-semibold text-sky-700 mb-4">📚 Zadnje sesije</h2>
            <div class="space-y-3">
              <div
                v-for="(l, i) in [...logs].reverse().slice(0,5)"
                :key="i"
                :class="darkMode ? 'bg-slate-700' : 'bg-sky-50 border border-sky-100'"
                class="p-3 rounded-xl"
              >
                <p class="font-medium">{{ l.subject}}</p>
                <p class="text-sm text-slate-500 mt-1">Fokus: {{ l.focus }} | Stres: {{ l.stress }}</p>
              </div>
            </div>
          </div>
        </div>

        <div
          :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mt-6"
        >
          <h2 class="text-xl font-semibold text-sky-700 mb-5">📈 Tjedni pregled</h2>
          <div class="space-y-4">
            <div v-for="d in chartData" :key="d.day">
              <div class="flex justify-between text-sm mb-1">
                <span>{{ d.day }}</span>
                <span class="text-slate-500">Fokus {{ d.productivity }}% / Stres {{ d.stress }}</span>
              </div>
              <div class="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
                <div class="bg-sky-500 h-3 rounded-full" :style="{ width: d.productivity + '%' }"></div>
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
import Sidebar from '../components/Sidebar.vue'
import api from '../../services/api'

const darkMode = ref(false)
const logs = ref([])
const aiAnalysis = ref('')
const username = ref("Student")

const loadStatistics = async () => {
  try {
    const response = await api.get('/statistics')

    console.log("DOBIVENI PODACI:", response.data)

    logs.value = response.data.history || []

  } catch (error) {
    console.error('Greška pri dohvaćanju statistike', error)
  }
}

const loadLatestAnalysis = async () => {
  try {
    const res = await api.get('/analyses')
    if (res.data.length > 0) {
      aiAnalysis.value = res.data[0].text
    } else {
      aiAnalysis.value = 'Još nema AI analiza.'
    }
  } catch (err) {
    console.error(err)
  }
}

const refreshData = async () => {
  try {
    await loadStatistics()

    const response = await api.get('/daily-analysis')

    aiAnalysis.value = response.data.analysis || 'Nema dostupne AI analize.'
    
  } catch (error) {
    console.error('Greška pri osvježavanju AI analize:', error)
  }
}

onMounted(() => {
  refreshData()
})

const optimalData = computed(() => {
  if (!logs.value.length) {
    return { hasData: false }
  }

  const subjects = {}

  logs.value.forEach(log => {
    const input = log.input || log

    const subject = log.subject || 'Opće učenje'

    if (!subjects[subject]) {
      subjects[subject] = []
    }

    subjects[subject].push({
      sleep_hours: Number(input.sleep_hours || 0),
      study_duration: Number(input.study_duration || 0),
      time_of_day: Number(input.time_of_day || 0),
      focus: Number(input.focus || 0),
      probability: Number(log.probability || 0)
    })
  })

  let bestSubject = null
  let bestScore = -1

  Object.entries(subjects).forEach(([subject, sessions]) => {
    const score =
      sessions.reduce(
        (sum, session) => sum + session.probability,
        0
      ) / sessions.length

    if (score > bestScore) {
      bestScore = score
      bestSubject = {
        name: subject,
        sessions
      }
    }
  })

  if (!bestSubject) {
    return { hasData: false }
  }

  const sessions = bestSubject.sessions

  const avgSleep =
    sessions.reduce(
      (sum, s) => sum + s.sleep_hours,
      0
    ) / sessions.length

  const avgDuration =
    sessions.reduce(
      (sum, s) => sum + s.study_duration,
      0
    ) / sessions.length

  const avgFocus =
    sessions.reduce(
      (sum, s) => sum + s.focus,
      0
    ) / sessions.length

  // 0 = Jutro, 1 = Podne, 2 = Popodne, 3 = Večer
  const times = {
    0: 'Jutro',
    1: 'Podne',
    2: 'Popodne',
    3: 'Večer'
  }

  const timeCounts = {}

  sessions.forEach(session => {
    const timeOfDay = session.time_of_day

    if (timeOfDay >= 0 && timeOfDay <= 3) {
      timeCounts[timeOfDay] =
        (timeCounts[timeOfDay] || 0) + 1
    }
  })

  let bestTime = null
  let bestCount = 0

  Object.entries(timeCounts).forEach(([timeOfDay, count]) => {
    if (count > bestCount) {
      bestTime = Number(timeOfDay)
      bestCount = count
    }
  })

  const time =
    bestTime !== null
      ? times[bestTime]
      : 'nije određeno'

  return {
    hasData: true,
    subject: bestSubject.name,
    sleep: avgSleep.toFixed(1),
    duration: Math.round(avgDuration),
    focus: avgFocus.toFixed(1),
    time
  }
})


const totalHours = computed(() => {
  const totalMinutes = logs.value.reduce((s, l) => s + Number(l.study_duration || 0), 0)
  return (totalMinutes / 60).toFixed(1)
})

const avgProductivity = computed(() => {
  if (!logs.value.length) return 0
  const avg = logs.value.reduce((s, l) => s + Number(l.probability || 0), 0) / logs.value.length
  return Math.round(avg * 100)
})

const avgFocus = computed(() => {
  if (!logs.value.length) return 0
  return (logs.value.reduce((s, l) => s + Number(l.focus || 0), 0) / logs.value.length).toFixed(1)
})

const avgStress = computed(() => {
  if (!logs.value.length) return 0
  return (logs.value.reduce((s, l) => s + Number(l.stress || 0), 0) / logs.value.length).toFixed(1)
})
const savedUser = localStorage.getItem("user")

if (savedUser) {
  const user = JSON.parse(savedUser)
  username.value = user.username
}
  
const chartData = computed(() => {
  const days = ['Pon', 'Uto', 'Sri', 'Čet', 'Pet', 'Sub', 'Ned']
  const recent = [...logs.value].slice(-7).reverse()

  return days.map((day, i) => {
    const entry = recent[i] || {}
    return {
      day,
      productivity: entry.probability ? Math.round(Number(entry.probability) * 100) : 0,
      stress: entry.stress || 0
    }
  })
})
</script>

<style>

</style>