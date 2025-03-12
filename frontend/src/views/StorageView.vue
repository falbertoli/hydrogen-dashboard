frontend/src/views/StorageView.vue
<template>
  <div>
    <h1>Storage Cost</h1>
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

<script>
import { storageService } from '../services/api.js';

export default {
  data() {
    return {
      formData: {
        total_h2_volume_gal: 1000,
        number_of_tanks: 10,
        tank_diameter_ft: 20,
        tank_length_ft: 40,
        cost_per_sqft_construction: 100,
        cost_per_cuft_insulation: 50,
      },
      result: null,
    };
  },
  methods: {
    async submitForm() {
      try {
        this.result = await storageService.calculateStorageCost(this.formData);
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },
  },
};
</script>
