<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >

    <div class="flex">

      <!-- SIDEBAR -->
      <aside
        :class="darkMode
          ? 'bg-slate-800 border-slate-700'
          : 'bg-white border-sky-100'"
        class="w-72 min-h-screen border-r p-5 hidden lg:block"
      >

        <div class="mb-8">
          <h1 class="text-3xl font-bold text-sky-600">
            StudyAI
          </h1>

          <p
            :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            class="text-sm mt-1"
          >
            Pametne studentske bilješke
          </p>
        </div>

        <!-- MENU -->
        <div class="space-y-2">

          <div class="p-3 rounded-xl hover:bg-sky-50 transition cursor-pointer text-slate-600">
            📊 Dashboard
          </div>

          <div class="p-3 rounded-xl hover:bg-sky-50 transition cursor-pointer text-slate-600">
            🧠 AI analiza
          </div>

          <div class="p-3 rounded-xl hover:bg-sky-50 transition cursor-pointer text-slate-600">
            ✍️ Zapisivanje
          </div>

          <div class="p-3 rounded-xl bg-sky-100 text-sky-700 font-medium cursor-pointer">
            📝 Bilješke
          </div>

          <div class="p-3 rounded-xl hover:bg-sky-50 transition cursor-pointer text-slate-600">
            📈 Statistika
          </div>

        </div>

      </aside>

      <!-- MAIN -->
      <main class="flex-1 p-6">

        <!-- HEADER -->
        <div class="flex justify-between items-center mb-8">

          <div>
            <h1 class="text-3xl font-bold text-sky-700">
              Bilješke 📝
            </h1>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-1"
            >
              Organiziraj svoje predmete i AI bilješke
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

          <!-- LEFT -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="lg:col-span-2 rounded-2xl border p-6 shadow-sm"
          >

            <h2 class="text-xl font-semibold text-sky-700 mb-5">
              Nova bilješka
            </h2>

            <!-- SUBJECT -->
            <div class="mb-5">

              <label class="text-sm text-slate-500">
                Predmet
              </label>

              <input
                v-model="subject"
                type="text"
                placeholder="npr. Matematika"
                :class="darkMode
                  ? 'bg-slate-700 border-slate-600 text-white'
                  : 'bg-sky-50 border-sky-100'"
                class="w-full mt-2 p-3 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none"
              />

            </div>

            <!-- NOTE -->
            <div class="mb-6">

              <label class="text-sm text-slate-500">
                Bilješka
              </label>

              <textarea
                v-model="text"
                placeholder="Upiši svoju bilješku..."
                :class="darkMode
                  ? 'bg-slate-700 border-slate-600 text-white'
                  : 'bg-sky-50 border-sky-100'"
                class="w-full mt-2 p-4 rounded-xl border focus:ring-2 focus:ring-sky-400 outline-none h-40 resize-none"
              ></textarea>

            </div>

            <!-- BUTTON -->
            <button
              @click="save"
              class="w-full bg-sky-500 hover:bg-sky-600 text-white py-4 rounded-xl font-semibold transition shadow-md"
            >
              Spremi bilješku
            </button>

          </div>

          <!-- RIGHT -->
          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm h-fit"
          >

            <h2 class="text-xl font-semibold text-sky-700 mb-5">
              🧠 AI Savjet
            </h2>

            <div class="space-y-4">

              <div class="bg-sky-50 border border-sky-100 rounded-2xl p-4">

                <h3 class="font-semibold text-sky-700 mb-2">
                  Organizacija
                </h3>

                <p class="text-sm text-slate-600 leading-relaxed">
                  Bilješke organizirane po predmetima povećavaju
                  učinkovitost ponavljanja gradiva.
                </p>

              </div>

              <div class="bg-emerald-50 border border-emerald-100 rounded-2xl p-4">

                <h3 class="font-semibold text-emerald-700 mb-2">
                  Preporuka
                </h3>

                <p class="text-sm text-slate-600 leading-relaxed">
                  Dodavanje kratkih sažetaka nakon svake sesije
                  može poboljšati dugoročno pamćenje.
                </p>

              </div>

            </div>

          </div>

        </div>

        <!-- SAVED NOTES -->
        <div
          :class="darkMode
            ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mt-6"
        >

          <div class="flex justify-between items-center mb-6">

            <h2 class="text-xl font-semibold text-sky-700">
              📚 Spremljene bilješke
            </h2>

            <div class="text-sm text-slate-500">
              Ukupno: {{ notes.length }}
            </div>

          </div>

          <!-- EMPTY -->
          <div
            v-if="notes.length === 0"
            class="text-center py-10 text-slate-400"
          >
            Nema spremljenih bilješki.
          </div>

          <!-- NOTES -->
          <div
            v-else
            class="grid grid-cols-1 md:grid-cols-2 gap-4"
          >

            <div
              v-for="(n, index) in notes"
              :key="index"
              :class="darkMode
                ? 'bg-slate-700 border-slate-600'
                : 'bg-sky-50 border-sky-100'"
              class="rounded-2xl border p-5"
            >

              <div class="flex justify-between items-start mb-3">

                <h3 class="font-semibold text-sky-700">
                  {{ n.subject }}
                </h3>

                <button
                  @click="removeNote(index)"
                  class="text-rose-400 hover:text-rose-500 transition"
                >
                  ✕
                </button>

              </div>

              <p
                :class="darkMode ? 'text-slate-300' : 'text-slate-600'"
                class="text-sm leading-relaxed whitespace-pre-line"
              >
                {{ n.text }}
              </p>

            </div>

          </div>

        </div>

      </main>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const darkMode = ref(false)

const subject = ref('')
const text = ref('')

const notes = ref(
  JSON.parse(localStorage.getItem("notes")) || []
)

function save() {

  if (!subject.value || !text.value) {
    alert("Unesi predmet i bilješku")
    return
  }

  notes.value.push({
    subject: subject.value,
    text: text.value
  })

  localStorage.setItem(
    "notes",
    JSON.stringify(notes.value)
  )

  subject.value = ''
  text.value = ''

  alert("Bilješka spremljena")
}

function removeNote(index) {

  notes.value.splice(index, 1)

  localStorage.setItem(
    "notes",
    JSON.stringify(notes.value)
  )
}
</script>

<style>

</style>