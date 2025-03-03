<!-- frontend/src/components/HydrogenDemandForm.vue -->
<template>
  <div class="form-container">
    <h2>Hydrogen Demand Calculator</h2>

    <form @submit.prevent="submitForm">
      <label>Percentage of Fleet Using Hydrogen: {{ fleetPercentage }}%</label>
      <input type="range" v-model="fleetPercentage" min="0" max="100" step="1" class="slider" />

      <label>Ground Vehicles:</label>
      <div class="vehicle-list">
        <div v-for="(vehicle, index) in selectedVehicles" :key="index" class="vehicle-row">
          <select v-model="vehicle.type" class="vehicle-type">
            <option v-for="v in vehicleOptions" :key="v" :value="v">{{ v }}</option>
          </select>
          <input type="number" v-model="vehicle.count" min="1" class="vehicle-quantity" placeholder="Quantity" />
          <button type="button" class="remove-btn" @click="removeVehicle(index)">❌</button>
        </div>
      </div>
      <button type="button" class="add-btn" @click="addVehicle">+ Add Vehicle</button>

      <label>Select Time Period:</label>
      <div class="time-selection">
        <select v-model="selectedTimePeriod" id="selectedTimePeriod">
          <option v-for="period in timePeriods" :key="period" :value="period">{{ period }}</option>
        </select>
        <select v-model="selectedYear" id="selectedYear">
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>
      <button type="submit">Calculate</button>
    </form>

    <div v-if="results" class="results">
      <h3>Results:</h3>
      <p>Estimated Hydrogen Demand: {{ results.estimatedH2Demand.toFixed(2) }} ft³</p>
      <p>Required Storage Area: {{ results.requiredStorageArea.toFixed(2) }} ft²</p>
      <p v-if="results.storageLocationFound">✔️ Suitable storage location found.</p>
      <!-- <HydrogenMap :requiredStorageArea="results.requiredStorageArea" /> -->
      <HydrogenMap :compliantZones="results?.compliantZones" :requiredStorageArea="results?.requiredStorageArea"
        v-if="results?.compliantZones && results?.compliantZones.length > 0" />
      <p v-else-if="results">❌ No suitable storage location available.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { submitHydrogenDemand } from "../composables/useHydrogenCalculator";
import HydrogenMap from "./HydrogenMap.vue";

// Reactive state
const fleetPercentage = ref(0);
const selectedVehicles = ref([]); // Fix: Ensure vehicles are reactive
const selectedTimePeriod = ref("7 days");
const selectedYear = ref("2025");
const results = ref(null);

// Ground vehicle options
const vehicleOptions = ref([
  "Pickup Truck", "Lavatory Service Truck", "Cargo Loader", "Fuel Truck", "Baggage Tug"
]);

// Time period options
const timePeriods = ref(["1 day", "2 days", "3 days", "4 days", "5 days", "6 days", "7 days"]);
const years = ref(["2025", "2030", "2035", "2040", "2045", "2050", "2055", "2060"]);

// Add or remove vehicle rows
const addVehicle = () => {
  selectedVehicles.value.push({ type: vehicleOptions.value[0], count: 1 });
};
const removeVehicle = (index) => {
  selectedVehicles.value.splice(index, 1);
};


// Submit form
const submitForm = async () => {
  // results.value = null; // Reset results before making the API call
  try {
    results.value = await submitHydrogenDemand(
      fleetPercentage.value,
      selectedVehicles.value,
      selectedTimePeriod.value
    );
  } catch (error) {
    console.error("Error submitting form:", error);
    alert("An error occurred while calculating the hydrogen demand.");
    results.value = {
      estimatedH2Demand: 0,
      requiredStorageArea: 0,
      storageLocationFound: false,
      compliantZones: [],
    };
  }
};
</script>

<style>
.slider {
  width: 100%;
  max-width: 475px;
  /* Match button width */
  display: block;
  margin: 0 auto;
  /* Center it */
  appearance: none;
  /* Remove default browser styles */
  height: 8px;
  /* Adjust thickness */
  border-radius: 5px;
  background: linear-gradient(to right, #444, #222);
  outline: none;
  border: none;
  transition: background 0.3s ease-in-out;
}

.slider:hover {
  background: linear-gradient(to right, #222, #000);
}

/* Webkit Browsers (Chrome, Safari) */
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 22px;
  /* Thumb size */
  height: 22px;
  background: #fff;
  border: 3px solid #007bff;
  /* Outline matching theme */
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  transition: all 0.2s ease-in-out;
}

.slider::-webkit-slider-thumb:hover {
  background: #007bff;
  border-color: #0056b3;
  box-shadow: 0 0 10px rgba(0, 86, 179, 0.8);
}

/* Firefox */
.slider::-moz-range-thumb {
  width: 22px;
  height: 22px;
  background: #fff;
  border: 3px solid #007bff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  transition: all 0.2s ease-in-out;
}

.slider::-moz-range-thumb:hover {
  background: #007bff;
  border-color: #0056b3;
  box-shadow: 0 0 10px rgba(0, 86, 179, 0.8);
}

.vehicle-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.vehicle-row select,
.vehicle-row input {
  flex: 1;
  height: 40px;
  /* Ensure uniform height */
  padding: 8px;
  margin-top: 17.5px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  /* Prevents padding from increasing height */
}

.vehicle-row select {
  flex: 4;
}

.vehicle-row input {
  flex: 1;
}

.vehicle-row input {
  text-align: center;
}

.remove-btn {
  width: 40px;
  height: 40px;
  margin-top: 11px;
  background: #b0b0b0;
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: #ff4d4d;
}

.time-selection {
  display: flex;
  gap: 15px;
  /* Space between dropdowns */
  justify-content: center;
  /* Centers them */
  align-items: center;
  width: 100%;
}

.time-selection select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

#selectedTimePeriod {
  flex: 2;
  /* Make this take more space */
  max-width: 300px;
  /* Adjust max width as needed */
}

#selectedYear {
  flex: 1;
  /* Make this smaller */
  max-width: 120px;
  /* Adjust max width as needed */
}
</style>
