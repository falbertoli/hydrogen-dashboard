<!-- frontend/src/components/HydrogenDemandForm.vue -->
<template>
  <div class="form-container">
    <h2>Hydrogen Demand Calculator</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>Percentage of Fleet Using Hydrogen: {{ fleetPercentage }}%</label>
        <input type="range" v-model="fleetPercentage" min="0" max="100" step="1" class="slider" />
      </div>

      <div class="form-group">
        <label>Ground Vehicles:</label>
        <div class="vehicle-list">
          <div v-for="(vehicle, index) in selectedVehicles" :key="index" class="vehicle-row">
            <select v-model="vehicle.type" class="vehicle-type">
              <!-- Use all vehicle options, but disable the ones already selected (except current) -->
              <option v-for="option in vehicleOptions" :key="option" :value="option"
                :disabled="isOptionDisabled(option, vehicle.type)">
                {{ option }}
              </option>
            </select>
            <button type="button" class="remove-btn" @click="removeVehicle(index)">❌</button>
          </div>
        </div>
        <button type="button" class="add-btn" @click="addVehicle" :disabled="!canAddMoreVehicles"
          :class="{ 'disabled': !canAddMoreVehicles }">
          + Add Vehicle
        </button>
        <p v-if="!canAddMoreVehicles" class="no-vehicles-message">
          All available vehicles have been added
        </p>
      </div>

      <div class="form-group">
        <label>Select End Year:</label>
        <div class="time-selection">
          <select v-model="selectedYear" id="selectedYear">
            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
      </div>

      <button type="submit">Calculate</button>
    </form>

    <div v-if="isLoading" class="loading">Loading...</div>
    <div v-if="results" class="results">
      <h3>Results:</h3>
      <p>Estimated Hydrogen Demand for Aircraft: {{ results?.aircraft_demand?.toFixed(2) || 0 }} ft³</p>
      <p>Estimated Hydrogen Demand for GSE: {{ results?.gse_demand?.total_h2_demand_vol_gse?.toFixed(2) || 0 }} ft³</p>
      <p>Total Estimated Hydrogen Demand: {{ results?.total_demand?.toFixed(2) || 0 }} ft³</p>

      <h3>Visualizations:</h3>
      <!-- Bar Chart: Aircraft vs. GSE Demand -->
      <div v-show="results.aircraft_demand && results.gse_demand?.total_h2_demand_vol_gse" class="chart-section">
        <h4>Aircraft vs. GSE Demand</h4>
        <Chart type="bar" :data="demandComparisonData" :options="demandComparisonOptions" />
      </div>

      <!-- Bar Chart: GSE Demand per Vehicle Type -->
      <div v-show="results.gse_demand?.gse_details?.length" class="chart-section">
        <h4>GSE Demand per Vehicle Type</h4>
        <Chart type="bar" :data="gseDemandPerVehicleData" :options="gseDemandPerVehicleOptions" />
      </div>

      <h3>Ground Support Equipment Details:</h3>
      <div v-for="(detail, index) in results?.gse_demand?.gse_details" :key="index" class="gse-detail">
        <p>Type: {{ detail.type }}</p>
        <p>Fuel Used: {{ detail.fuel_used }}</p>
        <p>Operating Time (Departure): {{ detail.operating_time_departure }} minutes</p>
        <p>Operating Time (Arrival): {{ detail.operating_time_arrival }} minutes</p>
        <p>Hydrogen Volume per Vehicle: {{ detail.hydrogen_volume_per_vehicle.toFixed(2) }} ft³</p>
      </div>
    </div>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { submitHydrogenDemand } from "@/api";
import Chart from "@/components/Chart.vue";

// Reactive state
const fleetPercentage = ref(0);
const selectedVehicles = ref([]);
const selectedYear = ref("2025");
const results = ref(null);
const error = ref(null);
const vehicleOptions = ref([]);
const isLoading = ref(false); // Add isLoading state

// Fetch vehicle options from CSV
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/data/ground_fleet_data.csv");
    const csvData = response.data;
    const lines = csvData.split("\n");
    lines.shift(); // Remove header
    vehicleOptions.value = lines.map(line => line.split(",")[0]);
  } catch (err) {
    console.error("Error fetching vehicle options:", err);
  }
});

// Helper function to check if an option should be disabled
const isOptionDisabled = (option, currentValue) => {
  // Don't disable the current value of this select
  if (option === currentValue) return false;

  // Disable if the option is already selected in another select
  return selectedVehicles.value.some(vehicle => vehicle.type === option);
};

// Computed property for available options
const availableVehicleOptions = computed(() => {
  const selectedTypes = new Set(selectedVehicles.value.map(v => v.type));
  return vehicleOptions.value.filter(option => !selectedTypes.has(option));
});

// Computed property to check if we can add more vehicles
const canAddMoreVehicles = computed(() => {
  return availableVehicleOptions.value.length > 0;
});

// Modified addVehicle function
const addVehicle = () => {
  if (availableVehicleOptions.value.length > 0) {
    selectedVehicles.value.push({
      type: availableVehicleOptions.value[0]
    });
  }
};

// Modified removeVehicle function
const removeVehicle = (index) => {
  selectedVehicles.value.splice(index, 1);
};


// Time period options
const years = ref(Array.from({ length: 28 }, (_, i) => 2023 + i));

// Submit form
const submitForm = async () => {
  results.value = null;
  error.value = null;
  isLoading.value = true; // Set loading state
  try {
    const response = await submitHydrogenDemand({
      slider_perc: fleetPercentage.value / 100,
      gse: selectedVehicles.value,
      end_year: parseInt(selectedYear.value)
    });
    results.value = response;
  } catch (err) {
    console.error("Error submitting form:", err);
    error.value = "An error occurred while calculating the hydrogen demand.";
  } finally {
    isLoading.value = false;
  }
};

// Chart Data and Options
const demandComparisonData = computed(() => {
  // Default empty data structure
  const defaultData = {
    labels: [],
    datasets: [{
      label: "Hydrogen Demand (ft³)",
      data: [],
      backgroundColor: ["#007bff", "#28a745"],
    }]
  };

  if (!results.value || !results.value.aircraft_demand) {
    return defaultData;
  }

  // Get the GSE demand value, ensuring it's a number
  const gseDemand = results.value.gse_demand &&
    typeof results.value.gse_demand.total_h2_demand_vol_gse !== 'undefined' ?
    Number(results.value.gse_demand.total_h2_demand_vol_gse) : 0;

  return {
    labels: ["Aircraft", "GSE"],
    datasets: [
      {
        label: "Hydrogen Demand (ft³)",
        data: [
          Number(results.value.aircraft_demand),
          gseDemand
        ],
        backgroundColor: ["#007bff", "#28a745"],
      },
    ],
  };
});

const gseDemandPerVehicleData = computed(() => {
  // Default empty data structure
  const defaultData = {
    labels: [],
    datasets: [{
      label: "Hydrogen Demand per Vehicle (ft³)",
      data: [],
      backgroundColor: "#28a745",
    }]
  };

  if (!results.value || !results.value.gse_demand || !results.value.gse_demand.gse_details ||
    !results.value.gse_demand.gse_details.length) {
    return defaultData;
  }

  return {
    labels: results.value.gse_demand.gse_details.map(detail => detail.type),
    datasets: [
      {
        label: "Hydrogen Demand per Vehicle (ft³)",
        data: results.value.gse_demand.gse_details.map(detail => detail.hydrogen_volume_per_vehicle),
        backgroundColor: "#28a745",
      },
    ],
  };
});

// Define the options as constants outside the template
const demandComparisonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: { display: true, text: "Aircraft vs. GSE Demand" },
    legend: { display: false },
  },
  scales: {
    y: { title: { display: true, text: "Demand (ft³)" }, beginAtZero: true },
  },
};

const gseDemandPerVehicleOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: { display: true, text: "GSE Demand per Vehicle Type" },
    legend: { display: false },
  },
  scales: {
    y: { title: { display: true, text: "Demand (ft³)" }, beginAtZero: true },
  },
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

input[type="range"] {
  width: 93%;
}

.form-group {
  width: 100%;
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.vehicle-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 10px;
}

.vehicle-type {
  flex: 13;
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.remove-btn {
  flex: 1;
  background: grey;
  color: white;
  border: none;
  border-radius: 4px;
  margin-top: 4px;
  padding: 8px;
  cursor: pointer;
}

.remove-btn:hover {
  background: #ff1a1a;
}

.add-btn {
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

.add-btn:hover {
  background: linear-gradient(135deg, #0056b3, #003d82);
  transform: scale(1.05);
}

.add-btn.disabled {
  background: linear-gradient(135deg, #cccccc, #999999);
  cursor: not-allowed;
  opacity: 0.7;
}

.add-btn.disabled:hover {
  transform: none;
  background: linear-gradient(135deg, #cccccc, #999999);
}

.no-vehicles-message {
  color: #666;
  font-style: italic;
  margin-top: 10px;
  font-size: 0.9em;
}

button[type="submit"] {
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

button[type="submit"]:hover {
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

.gse-detail {
  margin-top: 10px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  text-align: left;
  font-weight: normal;
  color: #333;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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

/* Existing styles */
.chart-section {
  margin-top: 20px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-section h4 {
  text-align: center;
  color: #333;
  margin-bottom: 10px;
}
</style>