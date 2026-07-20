<template>
  <div
    class="group bg-white dark:bg-slate-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 p-6 border border-slate-200 dark:border-slate-700"
  >
    <!-- Header -->

    <div class="flex justify-between items-start mb-5">

      <div class="flex items-center gap-3">

        <div>

          <h2
            class="text-xl font-bold text-slate-800 dark:text-white"
          >
            {{ subject.name }}
          </h2>

          <p
            class="text-slate-500 text-sm mt-1"
          >
            {{ subject.sessions }}
            sesija učenja
          </p>

        </div>

      </div>

      <!-- Productivity -->

      <span
        :class="badgeClass"
        class="px-3 py-1 rounded-full text-xs font-semibold"
      >
        {{ subject.productivity }} %
      </span>

    </div>

    <!-- Statistika -->

    <div class="space-y-4">

      <div class="flex justify-between">

        <span class="text-slate-500">
          ⭐ Fokus
        </span>

        <span class="font-semibold dark:text-white">
          {{ subject.avg_focus }}/10
        </span>

      </div>

      <div class="flex justify-between">

        <span class="text-slate-500">
          😵 Stres
        </span>

        <span class="font-semibold dark:text-white">
          {{ subject.avg_stress }}/10
        </span>

      </div>

      <div class="flex justify-between">

        <span class="text-slate-500">
          ⏱ Trajanje
        </span>

        <span class="font-semibold dark:text-white">
          {{ subject.avg_duration }} min
        </span>

      </div>

      <div class="flex justify-between">

        <span class="text-slate-500">
          📈 Produktivnost
        </span>

        <span class="font-semibold text-green-600">
          {{ subject.productivity }}%
        </span>

      </div>

    </div>

    <!-- Progress -->

    <div
      class="mt-6"
    >

      <div
        class="w-full h-3 rounded-full bg-slate-200 dark:bg-slate-700 overflow-hidden"
      >

        <div
          class="h-full rounded-full transition-all duration-700"
          :style="{
            width: subject.productivity + '%'
          }"
          :class="progressClass"
        />

      </div>

    </div>

    <!-- Footer -->

    <div
      class="mt-6 flex justify-between items-center"
    >

      <div>

        <p class="text-xs text-slate-500">
          Zadnje učenje
        </p>

        <p
          class="font-medium dark:text-white"
        >
          {{ subject.last_session }}
        </p>

      </div>

      <button
        @click="$emit('details', subject)"
        class="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-4 py-2 transition"
      >
        Detalji
      </button>

    </div>

  </div>
</template>

<script setup>

import { computed } from "vue";

const props = defineProps({

  subject: {

    type: Object,

    required: true

  }

});

defineEmits(["details"]);

const badgeClass = computed(() => {

  if (props.subject.productivity >= 85)

    return "bg-green-100 text-green-700";

  if (props.subject.productivity >= 70)

    return "bg-yellow-100 text-yellow-700";

  return "bg-red-100 text-red-700";

});

const progressClass = computed(() => {

  if (props.subject.productivity >= 85)

    return "bg-green-500";

  if (props.subject.productivity >= 70)

    return "bg-yellow-500";

  return "bg-red-500";

});


</script>

<style scoped>

button{

transition:.25s;

}

button:hover{

transform:translateY(-2px);

}

.group{

transition:.3s;

}

.group:hover{

border-color:#3b82f6;

}

</style>
