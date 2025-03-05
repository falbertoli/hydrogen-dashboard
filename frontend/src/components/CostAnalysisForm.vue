<!-- filepath: /c:/Users/alber/flask-vue-app/hydrogen-dashboard/frontend/src/components/CostAnalysisForm.vue -->
<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="fleetPercentage">Fleet Percentage: {{ fleetPercentage }}%</label>
        <input type="range" v-model.number="fleetPercentage" min="0" max="100" step="1" />
      </div>
      <div class="form-group">
        <label for="totalFlights">Total Flights per Year:</label>
        <input type="number" v-model.number="totalFlights" min="0" required />
      </div>
      <div class="form-group">
        <label for="atlantaFraction">Atlanta Fraction:</label>
        <input type="number" v-model.number="atlantaFraction" min="0" max="1" step="0.01" required />
      </div>
      <div class="form-group">
        <label for="hydrogenDemand">Hydrogen Demand (gallons):</label>
        <input type="number" v-model.number="hydrogenDemand" min="0" required />
      </div>
      <div class="form-group">
        <label for="turnaroundTime">Turnaround Time (minutes):</label>
        <input type="number" v-model.number="turnaroundTime" min="0" required />
      </div>
      <div class="form-group">
        <label for="taxCredits">Tax Credits ($/gallon):</label>
        <input type="number" v-model.number="taxCredits" min="0" step="0.01" required />
      </div>
      <button type="submit">Calculate</button>
    </form>

    <div v-if="results" class="results">
      <h3>Results:</h3>
      <p>Baseline Jet-A Utilization: {{ results.baseline_jetA_utilization }} hrs/yr</p>
      <p>Hydrogen Utilization: {{ results.hydrogen_utilization }} hrs/yr</p>
      <p>Baseline Revenue: ${{ results.baseline_revenue }} million</p>
      <p>New H2 Revenue: ${{ results.new_h2_revenue }} million</p>
      <p>Revenue Drop: ${{ results.revenue_drop }} million</p>
      <p>Total Tax Credits: ${{ results.total_tax_credits }} million</p>
      <p>Percent Revenue Drop: {{ results.percent_revenue_drop }}%</p>
    </div>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { submitFinancialAnalysis } from "../composables/useHydrogenCalculator";

const fleetPercentage = ref(30); // Default value based on provided logic
const totalFlights = ref(500000); // Default value based on provided logic
const atlantaFraction = ref(0.3); // Default value based on provided logic
const hydrogenDemand = ref(500 * 0.3 * 500000); // Default value based on provided logic
const turnaroundTime = ref(30); // Default value based on provided logic
const taxCredits = ref(1.0); // Default value based on provided logic
const results = ref(null);
const error = ref(null);

const submitForm = async () => {
  try {
    const data = {
      fleetPercentage: fleetPercentage.value / 100,
      totalFlights: totalFlights.value,
      atlantaFraction: atlantaFraction.value,
      hydrogenDemand: hydrogenDemand.value,
      turnaroundTime: turnaroundTime.value,
      taxCredits: taxCredits.value,
    };

    const response = await submitFinancialAnalysis(data);
    results.value = response.data;
    error.value = null; // Clear any previous errors
  } catch (err) {
    error.value = "An error occurred while submitting the form. Please try again.";
    results.value = null; // Clear any previous results
  }
};
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 50px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  width: 100%;
  margin-bottom: 15px;
  padding: 0 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

button {
  width: 100%;
  padding: 14px;
  margin-bottom: 15px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

button:hover {
  background: linear-gradient(135deg, #0056b3, #003d82);
  transform: scale(1.05);
}

.results {
  margin-top: 20px;
  padding: 18px;
  background: #e9f5ff;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  color: #0056b3;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.error {
  margin-top: 20px;
  padding: 18px;
  background: #ffdddd;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  color: #d8000c;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>