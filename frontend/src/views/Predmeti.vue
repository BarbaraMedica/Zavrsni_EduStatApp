<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 transition-colors duration-300"
  >
    <div class="flex">
      <Sidebar :darkMode="darkMode" />
      <!-- Glavni sadržaj -->
      <main class="flex-1 p-8 overflow-y-auto">

        <!-- Header -->
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8">

          <div>
            <h1
              class="text-4xl font-bold text-slate-800 dark:text-white flex items-center gap-3"
            >
              📚 Moji predmeti
            </h1>

            <p class="text-slate-500 dark:text-slate-400 mt-2">
              Pregled svih predmeta i analiza studentskih navika.
            </p>
          </div>

          <!-- Search -->
          <div class="mt-6 lg:mt-0 w-full lg:w-80">
            <input
              v-model="search"
              type="text"
              placeholder="Pretraži predmet..."
              class="w-full rounded-xl border border-slate-300 dark:border-slate-700
                     bg-white dark:bg-slate-800 px-4 py-3
                     focus:outline-none focus:ring-2 focus:ring-blue-500
                     dark:text-blue-500 transition-colors duration-300"
            />
          </div>

        </div>

        <!-- Dashboard kartice -->

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">

          <!-- Broj predmeta -->

          <div
            class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg border border-sky-200 dark:border-slate-600 p-6">
            <p class="text-sm text-slate-500">📚 Predmeti</p>

            <h2 class="text-3xl font-bold mt-2 dark:text-blue-500">
              {{ stats.subjects }}
            </h2>
          </div>

          <!-- Broj sesija -->

          <div
            class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg border border-sky-200 dark:border-slate-600 p-6"          >
            <p class="text-sm text-slate-500">📝 Sesije</p>

            <h2 class="text-3xl font-bold mt-2 dark:text-blue-500">
              {{ stats.sessions }}
            </h2>
          </div>

          <!-- Fokus -->

          <div
            class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg border border-sky-200 dark:border-slate-600 p-6"
          >
            <p class="text-sm text-slate-500">
              ⭐ Prosječan fokus
            </p>

            <h2 class="text-3xl font-bold mt-2 dark:text-blue-500">
              {{ stats.focus }}
            </h2>
          </div>

          <!-- Produktivnost -->

          <div
            class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg border border-sky-200 dark:border-slate-600 p-6"
          >
            <p class="text-sm text-slate-500">
              🧠 Produktivnost
            </p>

            <h2 class="text-3xl font-bold mt-2 dark:text-blue-500">
              {{ stats.productivity }}%
            </h2>
          </div>

        </div>

        <!-- Glavni sadržaj -->

        <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">

          <!-- Kartice -->

          <div class="xl:col-span-3">

            <div
              v-if="loading"
              class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg p-10 text-center"
            >
              <p class="text-lg dark:text-white">
                Učitavanje podataka...
              </p>
            </div>

            <div
              v-else-if="filteredSubjects.length === 0"
              class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg p-10 text-center"
            >
              <h2 class="text-2xl font-semibold dark:text-white mb-2">
                Nema pronađenih predmeta
              </h2>

              <p class="text-slate-500">
                Dodaj novu sesiju učenja kako bi se prikazali predmeti.
              </p>
            </div>

            <div
              v-else
              class="grid grid-cols-1 md:grid-cols-2 gap-6"
            >

              <PredmetiKartice
                v-for="subject in filteredSubjects"
                :key="subject.name"
                :subject="subject"
              />

            </div>

          </div>

          <!-- AI Panel -->

          <div>

            <div
              class="bg-gradient-to-br from-sky-50 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-2xl shadow-lg border border-sky-200 dark:border-slate-600 p-6 sticky top-6"
            >

              <h2
                class="text-xl font-bold dark:text-white flex items-center gap-2 mb-5"
              >
                🧠 AI Sažetak
              </h2>

              <div class="space-y-5">

                <div>

                  <p class="text-sm text-slate-500">
                    Najproduktivniji predmet
                  </p>

                  <p
                    class="font-semibold text-lg dark:text-blue-500 mt-1"
                  >
                    {{ bestSubject.name }}
                  </p>

                </div>

                <div>

                  <p class="text-sm text-slate-500">
                    Prosječan fokus
                  </p>

                  <p
                    class="font-semibold text-lg dark:text-blue-500 mt-1"
                  >
                    {{ bestSubject.avg_focus ?? '-' }}
                  </p>

                </div>

                <div>

                  <p class="text-sm text-slate-500">
                    AI preporuka
                  </p>

                  <p
                    class="text-slate-700 dark:text-slate-300 mt-2 leading-relaxed"
                  >
                    {{ aiRecommendation }}
                  </p>

                </div>

              </div>

            </div>

          </div>

        </div>

      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

import PredmetiKartice from "../components/PredmetiKartice.vue";
import Sidebar from '../components/Sidebar.vue'


const darkMode = ref(false);

const loading = ref(true);

const search = ref("");

const subjects = ref([]);

// API

const loadSubjects = async () => {
  loading.value = true;

  try {
    const response = await axios.get(
      "http://localhost:5000/subjects"
    );

    subjects.value = response.data;

  } catch (error) {

    console.error("Greška:", error);

  } finally {

    loading.value = false;

  }
};


const filteredSubjects = computed(() => {

  if (!search.value) return subjects.value;

  return subjects.value.filter(subject =>

    subject.name
      .toLowerCase()
      .includes(search.value.toLowerCase())

  );

});

// STATISTIKA

const stats = computed(() => {

  if (subjects.value.length === 0) {

    return {

      subjects: 0,
      sessions: 0,
      focus: 0,
      productivity: 0

    };

  }

  const totalSessions = subjects.value.reduce(
    (sum, subject) => sum + subject.sessions,
    0
  );

  const avgFocus = (

    subjects.value.reduce(
      (sum, subject) => sum + subject.avg_focus,
      0
    ) / subjects.value.length

  ).toFixed(1);

  const avgProductivity = (

    subjects.value.reduce(
      (sum, subject) => sum + subject.productivity,
      0
    ) / subjects.value.length

  ).toFixed(0);

  return {

    subjects: subjects.value.length,

    sessions: totalSessions,

    focus: avgFocus,

    productivity: avgProductivity

  };

});

const bestSubject = computed(() => {

  if (subjects.value.length === 0) {

    return {

      name: "-",

      avg_focus: "-"

    };

  }

  return [...subjects.value].sort(

    (a, b) =>

      b.productivity -

      a.productivity

  )[0];

});

const aiRecommendation = computed(() => {

  if (subjects.value.length === 0) {

    return "Dodajte prve sesije učenja kako bi umjetna inteligencija mogla analizirati vaše navike.";

  }

  return `Najveću produktivnost trenutno ostvarujete na predmetu "${bestSubject.value.name}". Nastavite održavati visoku razinu fokusa i dovoljno sna prije učenja.`;

});


onMounted(() => {

  loadSubjects();

});
</script>