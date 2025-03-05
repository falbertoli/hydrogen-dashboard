<!-- frontend/src/views/CostAnalysisView.vue -->
<template>
  <div class="cost-analysis-view">
    <h1>Cost Analysis</h1>
    <form @submit.prevent="submitForm">
      <!-- Add your form fields here -->
      <button type="submit">Submit</button>
    </form>
    <div v-if="result">
      <h2>Result</h2>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
import { submitFinancialAnalysis } from "../api";
import { ref } from 'vue';

const formData = ref({
  d: 1000,
  tax_credits: 1.0,
});
const result = ref(null);

async function submitForm() {
  try {
    result.value = await submitFinancialAnalysis(formData.value);
  } catch (error) {
    console.error("Error submitting form:", error);
  }
}
</script>

<style scoped>
.cost-analysis-view {
  padding: 20px;
}
</style>
