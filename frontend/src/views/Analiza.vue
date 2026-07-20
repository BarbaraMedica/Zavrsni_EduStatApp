<template>
  <div
    :class="darkMode ? 'bg-slate-900 text-white' : 'bg-sky-50 text-slate-800'"
    class="min-h-screen transition-all duration-300 p-6"
  >

    <Sidebar :darkMode="darkMode" />

    <div class="max-w-4xl mx-auto">

      <div
        class="bg-white rounded-2xl shadow-sm border border-sky-100 p-8"
        :class="darkMode ? 'bg-slate-800 border-slate-700' : ''"
      >

        <h1 class="text-2xl font-bold mb-6">
          AI analiza učenja
        </h1>


        <!-- INPUT FORMA -->

        <div class="grid grid-cols-2 gap-4">


          <div>
            <label>Datum</label>
            <input
              v-model="form.date"
              type="date"
              class="input"
            />
          </div>


          <div>
            <label>Predmet</label>
            <input
              v-model="form.subject"
              type="text"
              placeholder="npr. Matematika"
              class="input"
            />
          </div>


          <div>
            <label>Sati sna</label>
            <input
              v-model.number="form.sleep_hours"
              type="number"
              class="input"
            />
          </div>


          <div>
            <label>Trajanje učenja (min)</label>
            <input
              v-model.number="form.study_duration"
              type="number"
              class="input"
            />
          </div>


          <div>
            <label>Broj pauza</label>

            <input
              v-model.number="form.breaks"
              type="number"
              class="input"
            />

          </div>



          <div>

            <label>Dio dana</label>

            <select
              v-model.number="form.time_of_day"
              class="input"
            >

              <option :value="0">
                Jutro
              </option>

              <option :value="1">
                Podne
              </option>

              <option :value="2">
                Popodne
              </option>

              <option :value="3">
                Večer
              </option>

            </select>

          </div>




          <div>

            <label>Fokus (1-10)</label>

            <input
              v-model.number="form.focus"
              type="number"
              min="1"
              max="10"
              class="input"
            />

          </div>



          <div>

            <label>Stres (1-10)</label>

            <input
              v-model.number="form.stress"
              type="number"
              min="1"
              max="10"
              class="input"
            />

          </div>



          <div>

            <label>Energija (1-10)</label>

            <input
              v-model.number="form.energy"
              type="number"
              min="1"
              max="10"
              class="input"
            />

          </div>


        </div>



        <!-- BUTTON -->

        <button
          @click="predict"
          :disabled="loading"
          class="mt-6 w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl"
        >

          {{ loading ? "Analiziram..." : "Pokreni AI analizu" }}

        </button>



        <!-- REZULTAT -->


        <div
          v-if="result"
          class="mt-8 p-6 rounded-xl border"
          :class="resultClass"
        >


          <h2 class="text-xl font-bold mb-3">
            Rezultat modela
          </h2>


          <p class="text-lg">
            {{ result }}
          </p>


          <p class="mt-2">
            Vjerojatnost:
            <strong>
              {{ probability }}%
            </strong>
          </p>



          <hr class="my-5">



          <h2 class="text-xl font-bold mb-3">
            AI preporuka
          </h2>



          <p class="whitespace-pre-line">
            {{ advice }}
          </p>


        </div>



      </div>

    </div>

  </div>
</template>




<script setup>

import { ref } from "vue"
import axios from "axios"
import Sidebar from "../components/Sidebar.vue"



const darkMode = ref(false)



const loading = ref(false)



const form = ref({

  date:
    new Date()
    .toISOString()
    .split("T")[0],


  subject:"",


  sleep_hours:7,


  study_duration:90,


  breaks:2,


  time_of_day:0,


  focus:7,


  stress:4,


  energy:8

})




const result = ref("")
const probability = ref("")
const advice = ref("")

const resultClass = ref("")






async function predict(){


  try{


    loading.value=true



    const response = await axios.post(

      "http://127.0.0.1:5000/analyze",

      form.value

    )



    result.value =
      response.data.prediction



    probability.value =
      response.data.probability



    advice.value =
      response.data.ai_analysis




    if(
      result.value
      .toLowerCase()
      .includes("dobro")
    ){

      resultClass.value =
        "bg-green-50 border-green-200 text-green-800"

    }

    else{

      resultClass.value =
        "bg-red-50 border-red-200 text-red-800"

    }



  }


  catch(error){


    console.error(error)


    alert(
      "Greška pri povezivanju s AI analizom"
    )


  }


  finally{

    loading.value=false

  }


}



</script>





<style scoped>


.input{

  width:100%;
  padding:10px;
  margin-top:5px;

  border-radius:10px;

  border:1px solid #cbd5e1;

  background:white;

}


label{

  font-size:14px;

  font-weight:600;

}


</style>