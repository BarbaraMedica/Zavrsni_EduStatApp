<template>
  <div class="app">

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Analiza from './views/Analiza.vue'
import Statistika from './views/Statistika.vue'
import Biljeske from './views/Biljeske.vue'
import Dashboard from './views/Dashboard.vue'

const current = ref('analiza')
</script>

<style>
.app {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background: #edeef1;
  color: rgb(8, 98, 136);
  padding: 20px;
  border-radius: 12px;
  margin-left: 30px;
}

.sidebar button {
  display: block;
  margin: 10px 0;
  width: 100%;
  padding: 10px;
  color: rgb(8, 98, 136);
  background: white;
  border: 1px solid #ccc;
}

.content {
  flex: 1;
  padding: 30px;
  background: #f9fafb;
}
</style>