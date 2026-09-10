<template>
  <div class="min-h-screen bg-sky-50 flex items-center justify-center p-6">

    <div class="bg-white w-full max-w-md rounded-2xl shadow-lg p-8">

      <h1 class="text-3xl font-bold mb-2">
        EduStat
      </h1>

      <p class="text-slate-500 mb-8">
        Prijava korisnika
      </p>

      <form @submit.prevent="login">

        <label class="block mb-2 font-semibold">
          Email
        </label>

        <input
          v-model="email"
          type="email"
          class="w-full p-3 border rounded-xl mb-5"
          required
        />

        <label class="block mb-2 font-semibold">
          Lozinka
        </label>

        <input
          v-model="password"
          type="password"
          class="w-full p-3 border rounded-xl mb-5"
          required
        />

        <p
          v-if="error"
          class="text-red-600 mb-4"
        >
          {{ error }}
        </p>

        <button
          type="submit"
          class="w-full bg-sky-600 text-white p-3 rounded-xl font-semibold"
        >
          Prijavi se
        </button>

      </form>

      <p class="text-center mt-6">
        Nemaš račun?

        <router-link
          to="/register"
          class="text-sky-600 font-semibold"
        >
          Registriraj se
        </router-link>
      </p>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const email = ref("")
const password = ref("")

const error = ref("")


async function login() {

  error.value = ""

  try {

    const response = await axios.post(
      "http://127.0.0.1:5000/auth/login",
      {
        email: email.value,
        password: password.value
      }
    )

    // spremi JWT
    localStorage.setItem(
      "token",
      response.data.token
    )

    // spremi podatke korisnika
    localStorage.setItem(
      "user",
      JSON.stringify(response.data.user)
    )

    // idi na Dashboard
    router.push("/dashboard")

  } catch (err) {

    error.value =
      err.response?.data?.error ||
      "Greška pri prijavi."

  }

}

</script>