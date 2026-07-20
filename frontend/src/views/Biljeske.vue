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
              Povijest AI analiza 🧠
            </h1>


            <p
              :class="darkMode ? 'text-slate-400' : 'text-slate-500'"
              class="mt-1"
            >
              Pregled spremljenih analiza, zaključaka i AI preporuka
            </p>


          </div>



          <button
            @click="darkMode = !darkMode"
            class="bg-sky-500 hover:bg-sky-600 text-white px-4 py-2 rounded-xl transition"
          >
            {{ darkMode ? '☀️ Light' : '🌙 Dark' }}
          </button>


        </div>





        <!-- GRID -->

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">


          <!-- NEW ANALYSIS -->

          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="lg:col-span-2 rounded-2xl border p-6 shadow-sm"
          >


            <h2 class="text-xl font-semibold text-sky-700 mb-5">
              Nova analiza
            </h2>



            <label class="text-sm text-slate-500">
              Predmet
            </label>


            <input
              v-model="subject"
              placeholder="npr. Strojno učenje"
              :class="darkMode
                ? 'bg-slate-700 border-slate-600 text-white'
                : 'bg-sky-50 border-sky-100'"
              class="w-full mt-2 mb-5 p-3 rounded-xl border outline-none focus:ring-2 focus:ring-sky-400"
            />




            <label class="text-sm text-slate-500">
              Rezultat analize
            </label>


            <textarea

              v-model="text"

              placeholder="Unesi rezultat AI analize..."

              :class="darkMode
                ? 'bg-slate-700 border-slate-600 text-white'
                : 'bg-sky-50 border-sky-100'"

              class="w-full mt-2 p-4 rounded-xl border h-40 resize-none outline-none focus:ring-2 focus:ring-sky-400"

            ></textarea>




            <button
              @click="save"
              class="w-full mt-6 bg-sky-500 hover:bg-sky-600 text-white py-4 rounded-xl font-semibold transition"
            >

              Spremi analizu

            </button>


          </div>





          <!-- AI INFO -->


          <div
            :class="darkMode
              ? 'bg-slate-800 border-slate-700'
              : 'bg-white border-sky-100'"
            class="rounded-2xl border p-6 shadow-sm h-fit"
          >


            <h2 class="text-xl font-semibold text-sky-700 mb-5">
              🤖 AI pomoć
            </h2>



            <div class="bg-sky-50 rounded-2xl p-4 mb-4">


              <h3 class="font-semibold text-sky-700">
                Analiza znanja
              </h3>


              <p class="text-sm text-slate-600 mt-2">
                Spremljene analize omogućuju praćenje područja
                koja student treba dodatno ponoviti.
              </p>


            </div>



            <div class="bg-emerald-50 rounded-2xl p-4">


              <h3 class="font-semibold text-emerald-700">
                Preporuka
              </h3>


              <p class="text-sm text-slate-600 mt-2">
                Redovito analiziranje rezultata pomaže
                poboljšanju procesa učenja.
              </p>


            </div>



          </div>



        </div>





        <!-- HISTORY -->


        <div
          :class="darkMode
            ? 'bg-slate-800 border-slate-700'
            : 'bg-white border-sky-100'"
          class="rounded-2xl border p-6 shadow-sm mt-6"
        >


          <div class="flex justify-between items-center mb-6">


            <h2 class="text-xl font-semibold text-sky-700">
              📚 Spremljene analize
            </h2>


            <span class="text-sm text-slate-500">
              Ukupno: {{ analyses.length }}
            </span>


          </div>





          <div
            v-if="analyses.length === 0"
            class="text-center py-10 text-slate-400"
          >

            Nema spremljenih analiza.

          </div>






          <div
            v-else
            class="grid grid-cols-1 md:grid-cols-2 gap-5"
          >



            <div
              v-for="(item,index) in analyses"
              :key="index"

              :class="darkMode
                ? 'bg-slate-700 border-slate-600'
                : 'bg-sky-50 border-sky-100'"

              class="rounded-2xl border p-5"
            >



              <div class="flex justify-between mb-3">


                <h3 class="font-semibold text-sky-700">
                  📚 {{ item.subject }}
                </h3>



                <button
                  @click="removeAnalysis(index)"
                  class="text-rose-400 hover:text-rose-500"
                >

                  ✕

                </button>


              </div>




              <p class="text-xs text-slate-500 mb-3">
                {{ item.date }}
              </p>




              <p
                :class="darkMode ? 'text-slate-300' : 'text-slate-600'"
                class="text-sm whitespace-pre-line leading-relaxed"
              >

                {{ item.text }}

              </p>



              <div
                class="mt-4 bg-white/50 rounded-xl p-3 text-sm"
              >

                💡 AI preporuka:
                Nastaviti pratiti napredak i ponoviti ključne dijelove gradiva.

              </div>



            </div>



          </div>



        </div>


      </main>


    </div>

  </div>
</template>





<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'

const darkMode = ref(false)



const subject = ref('')
const text = ref('')



const analyses = ref([])
const apiBase = 'http://127.0.0.1:5000'

const loadAnalyses = async () => {
  try {
    const response = await axios.get(`${apiBase}/analyses`)
    analyses.value = response.data
  } catch (error) {
    console.error('Greška pri dohvaćanju analiza', error)
    alert('Greška pri učitavanjem analiza.')
  }
}





function save(){


  if(!subject.value || !text.value){

    alert("Unesi predmet i rezultat analize")

    return

  }



  analyses.value.push({

    subject: subject.value,

    text:text.value,

    date:new Date()
      .toLocaleDateString("hr-HR"),

    type:"AI analiza"

  })



  localStorage.setItem(
    "analyses",
    JSON.stringify(analyses.value)
  )



  subject.value=''
  text.value=''



}






function removeAnalysis(index){


  analyses.value.splice(index,1)



  localStorage.setItem(
    "analyses",
    JSON.stringify(analyses.value)
  )


}



</script>