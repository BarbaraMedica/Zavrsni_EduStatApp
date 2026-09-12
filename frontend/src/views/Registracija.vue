
<template>
  <div class="min-h-screen bg-sky-50 flex items-center justify-center p-6">

    <div class="bg-white w-full max-w-md rounded-2xl shadow-lg p-8">

      <h1 class="text-3xl font-bold mb-2">
        EduStat
      </h1>

      <p class="text-slate-500 mb-8">
        Registracija korisnika
      </p>

      <form @submit.prevent="register">

        <label class="block mb-2 font-semibold">
          Korisničko ime
        </label>

        <input
          v-model="username"
          class="w-full p-3 border rounded-xl mb-5"
          required
        />

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
          minlength="6"
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
          Registriraj se
        </button>

      </form>

      <p class="text-center mt-6">

        Već imaš račun?

        <router-link
          to="/"
          class="text-sky-600 font-semibold"
        >
          Prijavi se
        </router-link>

      </p>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../../services/api"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")

const error = ref("")


async function register() {

  error.value = ""

  try {

    await api.post(
      "/auth/register",
      {
        username: username.value,
        email: email.value,
        password: password.value
      }
    )
    

    alert("Registracija uspješna!")

    router.push("/")

  } catch (err) {

    error.value =
      err.response?.data?.error ||
      "Greška pri registraciji."

  }

}

</script>