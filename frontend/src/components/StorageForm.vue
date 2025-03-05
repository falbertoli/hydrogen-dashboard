<!-- frontend/src/components/StorageForm.vue -->
<template>
  <div class="form-container">
    <h2>Storage Capacity Calculator</h2>

    <form @submit.prevent="submitForm">
      <div class="storage-inputs">
        <label>Available Storage Area (sq ft):</label>
        <input type="number" v-model.number="storageArea" min="0" required />
        <button type="submit">Calculate</button>
      </div>
    </form>

    <div v-if="results" class="results">
      <h3>Results:</h3>
      <p v-if="results.maxHydrogenStored !== undefined">
        Max Hydrogen Demand from Storage: {{ results.maxHydrogenStored.toFixed(2) }} ft³
      </p>
      <p v-else>⚠️ No valid result received.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { submitStorage } from "../composables/useHydrogenCalculator";

const storageArea = ref(0);
const results = ref(null);

const submitForm = async () => {
  results.value = await submitStorage(storageArea.value);
  console.log("API Response:", results.value);  // Debugging
};
</script>

<style>
.storage-inputs {
  display: flex;
  flex-direction: column;
  /* Ensures label and input stay in a vertical column */
  align-items: flex-start;
  /* Aligns items to the left */
  gap: 5px;
  /* Adds a small gap between label and input */
  margin-bottom: 15px;
  /* Adds space before the button */
}

.storage-inputs label {
  font-weight: bold;
  color: #333;
}

.storage-inputs input {
  width: 100%;
  /* Makes sure the input takes full width */
  max-width: 250px;
  /* Adjust the max width */
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>