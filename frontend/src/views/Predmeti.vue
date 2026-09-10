<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-gradient-to-br from-slate-50 to-blue-50 text-slate-800'"
    class="min-h-screen transition-colors duration-300"
  >
    <div class="flex">
      <Sidebar :darkMode="darkMode" />
      <!-- Glavni sadržaj -->
      <main class="flex-1 p-8 overflow-y-auto">

        <!-- Header -->
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8">

          <div>
            <h1
              class="text-4xl font-bold flex items-center gap-3"
              :class="darkMode ? 'text-white' : 'text-slate-800'"
            >
              📚 Moji predmeti
            </h1>

            <p
              class="mt-2"
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >
              Pregled svih predmeta i analiza studentskih navika.
            </p>
          </div>

          <div class="mt-6 lg:mt-0 flex items-center gap-3 w-full lg:w-auto">
            <div class="w-full lg:w-80">
              <input
                v-model="search"
                type="text"
                placeholder="Pretraži predmet..."
                :class="darkMode
                  ? 'bg-slate-800 border-slate-700 text-white placeholder:text-slate-400'
                  : 'bg-white border-slate-300 text-slate-700 placeholder:text-slate-400'"
                class="w-full rounded-xl border px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-300"
              />
            </div>

            <button
              @click="darkMode = !darkMode; localStorage.setItem('darkMode', String(darkMode))"
              class="bg-slate-700 hover:bg-slate-800 text-white px-4 py-2 rounded-xl transition"
            >
              Dark
            </button>
          </div>

        </div>

        <!-- Dashboard kartice -->

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">

          <!-- Broj predmeta -->

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gradient-to-br from-sky-50 to-blue-100 border-sky-200'"
            class="rounded-2xl shadow-lg border p-6"
          >
            <p
              class="text-sm"
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >📚 Predmeti</p>

            <h2
              class="text-3xl font-bold mt-2"
              :class="darkMode ? 'text-sky-400' : 'text-slate-800'"
            >
              {{ stats.subjects }}
            </h2>
          </div>

          <!-- Broj sesija -->

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gradient-to-br from-sky-50 to-blue-100 border-sky-200'"
            class="rounded-2xl shadow-lg border p-6"
          >
            <p
              class="text-sm"
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >📝 Sesije</p>

            <h2
              class="text-3xl font-bold mt-2"
              :class="darkMode ? 'text-sky-400' : 'text-slate-800'"
            >
              {{ stats.sessions }}
            </h2>
          </div>

          <!-- Fokus -->

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gradient-to-br from-sky-50 to-blue-100 border-sky-200'"
            class="rounded-2xl shadow-lg border p-6"
          >
            <p
              class="text-sm"
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >
              ⭐ Prosječan fokus
            </p>

            <h2
              class="text-3xl font-bold mt-2"
              :class="darkMode ? 'text-sky-400' : 'text-slate-800'"
            >
              {{ stats.focus }}
            </h2>
          </div>

          <!-- Produktivnost -->

          <div
            :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gradient-to-br from-sky-50 to-blue-100 border-sky-200'"
            class="rounded-2xl shadow-lg border p-6"
          >
            <p
              class="text-sm"
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >
              🧠 Produktivnost
            </p>

            <h2
              class="text-3xl font-bold mt-2"
              :class="darkMode ? 'text-sky-400' : 'text-slate-800'"
            >
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
              :class="darkMode ? 'bg-slate-800' : 'bg-gradient-to-br from-sky-50 to-blue-100'"
              class="rounded-2xl shadow-lg p-10 text-center"
            >
              <p :class="darkMode ? 'text-white' : 'text-slate-700'" class="text-lg">
                Učitavanje podataka...
              </p>
            </div>

            <div
              v-else-if="filteredSubjects.length === 0"
              :class="darkMode ? 'bg-slate-800' : 'bg-gradient-to-br from-sky-50 to-blue-100'"
              class="rounded-2xl shadow-lg p-10 text-center"
            >
              <h2
                class="text-2xl font-semibold mb-2"
                :class="darkMode ? 'text-white' : 'text-slate-800'"
              >
                Nema pronađenih predmeta
              </h2>

              <p :class="darkMode ? 'text-slate-400' : 'text-slate-500'">
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
              :class="darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gradient-to-br from-sky-50 to-blue-100 border-sky-200'"
              class="rounded-2xl shadow-lg border p-6 sticky top-6"
            >

              <h2
                class="text-xl font-bold flex items-center gap-2 mb-5"
                :class="darkMode ? 'text-white' : 'text-slate-800'"
              >
                🧠 AI Sažetak
              </h2>

              <div class="space-y-5">

                <div>

                  <p
                    class="text-sm"
                    :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
                  >
                    Najproduktivniji predmet
                  </p>

                  <p
                    class="font-semibold text-lg mt-1"
                    :class="darkMode ? 'text-sky-400' : 'text-sky-700'"
                  >
                    {{ bestSubject.name }}
                  </p>

                </div>

                <div>

                  <p
                    class="text-sm"
                    :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
                  >
                    Prosječan fokus
                  </p>

                  <p
                    class="font-semibold text-lg mt-1"
                    :class="darkMode ? 'text-sky-400' : 'text-sky-700'"
                  >
                    {{ bestSubject.avg_focus ?? '-' }}
                  </p>

                </div>

                <div>

                  <p
                    class="text-sm"
                    :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
                  >
                    AI preporuka
                  </p>

                  <p
                    class="mt-2 leading-relaxed"
                    :class="darkMode ? 'text-slate-300' : 'text-slate-700'"
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
import PredmetiKartice from "../components/PredmetiKartice.vue";
import Sidebar from '../components/Sidebar.vue'
import api from "../../services/api";

const darkMode = ref(localStorage.getItem("darkMode") === "true");

const loading = ref(true);

const search = ref("");

const subjects = ref([]);

// API

const loadSubjects = async () => {
  loading.value = true;

  try {
    const response = await api.get(
      "/subjects"
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