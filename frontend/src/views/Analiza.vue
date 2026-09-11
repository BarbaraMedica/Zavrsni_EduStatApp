<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300"
  >
    <div class="flex">

      <Sidebar :darkMode="darkMode" />

      <main class="flex-1 p-6">

        <div class="max-w-7xl mx-auto">

          <div class="flex justify-between items-center mb-8">
            <div>
              <h1
                class="text-3xl font-bold"
                :class="darkMode ? 'text-white' : 'text-slate-800'"
              >
                AI Analiza
              </h1>

              <p
                class="mt-2"
                :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              >
                Detaljna analiza tvojih navika učenja pomoću umjetne inteligencije.
              </p>
            </div>

            <div class="flex items-center gap-3">
              <button
                @click="loadFullAnalysis"
                :disabled="loading"
                class="px-5 py-3 rounded-xl font-semibold transition"
                :class="
                  loading
                    ? 'bg-slate-400 cursor-not-allowed text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                "
              >
                {{ loading ? "Analiziram..." : "Osvježi analizu" }}
              </button>

              <button
                @click="darkMode = !darkMode; localStorage.setItem('darkMode', String(darkMode))"
                class="bg-slate-700 hover:bg-slate-800 text-white px-4 py-2 rounded-xl transition"
              >
                {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
              </button>
            </div>
          </div>

          <div
            v-if="error"
            class="mb-6 p-4 rounded-xl border"
            :class="
              darkMode
                ? 'bg-red-900/30 border-red-700 text-red-300'
                : 'bg-red-50 border-red-200 text-red-700'
            "
          >
            {{ error }}
          </div>

          <div
            v-if="loading"
            class="rounded-2xl p-8 mb-6 text-center shadow"
            :class="
              darkMode
                ? 'bg-slate-800'
                : 'bg-white'
            "
          >
            <div class="text-4xl mb-4">
              
            </div>

            <h2 class="text-xl font-semibold mb-2">
              AI analizira tvoje podatke...
            </h2>

            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
            >
              Analiziraju se posljednje sesije učenja, predmeti, san,
              fokus, stres, energija, trajanje učenja i rezultati modela.
            </p>
          </div>

          <div
            v-if="!loading && analysis"
            class="rounded-2xl p-6 shadow mb-8"
            :class="
              darkMode
                ? 'bg-slate-800'
                : 'bg-white'
            "
          >
            <div class="flex items-center gap-3 mb-6">
              <div
                class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                :class="
                  darkMode
                    ? 'bg-blue-900/40'
                    : 'bg-blue-100'
                "
              >
                
              </div>

              <div>
                <h2 class="text-2xl font-bold">
                  Detaljna AI analiza
                </h2>

                <p
                  class="text-sm"
                  :class="
                    darkMode
                      ? 'text-slate-400'
                      : 'text-slate-500'
                  "
                >
                  Analiza posljednjih 10 sesija učenja
                </p>
              </div>
            </div>

            <div
              class="max-w-none leading-7 whitespace-pre-line"
              :class="darkMode ? 'text-slate-200' : 'text-slate-700'"
            >
              {{ analysis || 'Nema dostupne detaljne analize.' }}
            </div>
          </div>

          <div
            v-if="!loading && sessions.length > 0"
            class="rounded-2xl p-6 shadow"
            :class="
              darkMode
                ? 'bg-slate-800'
                : 'bg-white'
            "
          >
            <div class="flex justify-between items-center mb-6">
              <div>
                <h2 class="text-2xl font-bold">
                  Analizirane sesije
                </h2>

                <p
                  class="text-sm mt-1"
                  :class="
                    darkMode
                      ? 'text-slate-400'
                      : 'text-slate-500'
                  "
                >
                  Podaci koji su korišteni za izradu AI analize
                </p>
              </div>

              <span
                class="px-3 py-1 rounded-full text-sm font-semibold"
                :class="
                  darkMode
                    ? 'bg-blue-900/40 text-blue-300'
                    : 'bg-blue-100 text-blue-700'
                "
              >
                {{ sessions.length }} sesija
              </span>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr
                    class="border-b"
                    :class="
                      darkMode
                        ? 'border-slate-700'
                        : 'border-slate-200'
                    "
                  >
                    <th class="py-3 px-3">Predmet</th>
                    <th class="py-3 px-3">Trajanje</th>
                    <th class="py-3 px-3">San</th>
                    <th class="py-3 px-3">Fokus</th>
                    <th class="py-3 px-3">Stres</th>
                    <th class="py-3 px-3">Energija</th>
                    <th class="py-3 px-3">Predikcija</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="(session, index) in sessions"
                    :key="session._id || session.date || index"
                    class="border-b last:border-b-0"
                    :class="
                      darkMode
                        ? 'border-slate-700'
                        : 'border-slate-100'
                    "
                  >
                    <td class="py-4 px-3 font-medium">
                      {{ session.subject || "Nije uneseno" }}
                    </td>

                    <td class="py-4 px-3">
                      {{ session.study_duration ?? "—" }}
                      <span v-if="session.study_duration">
                        min
                      </span>
                    </td>

                    <td class="py-4 px-3">
                      {{ session.sleep_hours ?? "—" }}
                      <span v-if="session.sleep_hours">
                        h
                      </span>
                    </td>

                    <td class="py-4 px-3">
                      {{ session.focus_level ?? "—" }}
                    </td>

                    <td class="py-4 px-3">
                      {{ session.stress_level ?? "—" }}
                    </td>

                    <td class="py-4 px-3">
                      {{ session.energy_level ?? "—" }}
                    </td>

                    <td class="py-4 px-3">
                      <span
                        v-if="session.prediction"
                        class="px-3 py-1 rounded-lg text-sm font-medium"
                        :class="
                          darkMode
                            ? 'bg-green-900/40 text-green-300'
                            : 'bg-green-100 text-green-700'
                        "
                      >
                        {{ session.prediction }}
                      </span>

                      <span v-else>
                        —
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div
            v-if="!loading && !analysis && sessions.length === 0"
            class="rounded-2xl p-10 text-center shadow"
            :class="
              darkMode
                ? 'bg-slate-800'
                : 'bg-white'
            "
          >
            <div class="text-5xl mb-4">
              📊
            </div>

            <h2 class="text-xl font-bold mb-2">
              Nema dovoljno podataka
            </h2>

            <p
              :class="
                darkMode
                  ? 'text-slate-400'
                  : 'text-slate-500'
              "
            >
              Zabilježi nekoliko sesija učenja kako bi AI mogao
              napraviti detaljnu analizu tvojih navika.
            </p>
          </div>

        </div>

      </main>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import Sidebar from "../components/Sidebar.vue";
import api from "../../services/api";

export default {
  name: "AIAnalysis",

  components: {
    Sidebar
  },

  setup() {
    const analysis = ref("");
    const sessions = ref([]);
    const loading = ref(false);
    const error = ref("");

    const darkMode = ref(
      localStorage.getItem("darkMode") === "true"
    );

    const syncDarkMode = () => {
      localStorage.setItem("darkMode", String(darkMode.value));
    };

    watch(darkMode, () => {
      syncDarkMode();
    }, { immediate: true });

    const loadFullAnalysis = async () => {
      loading.value = true;
      error.value = "";

      try {
        const response = await api.get("/full-analysis");

        analysis.value = response.data.analysis || "";
        sessions.value = response.data.sessions || [];

      } catch (err) {
        console.error("Greška kod dohvaćanja AI analize:", err);

        if (err.response?.status === 401) {
          error.value = "Sesija je istekla. Prijavi se ponovno.";
        } else {
          error.value =
            err.response?.data?.error ||
            "Dogodila se greška prilikom dohvaćanja AI analize.";
        }
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      loadFullAnalysis();
    });

    return {
      analysis,
      sessions,
      loading,
      error,
      darkMode,
      loadFullAnalysis
    };
  }
};
</script>