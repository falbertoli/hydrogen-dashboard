<!-- frontend/src/components/HydrogenDemandForm.vue -->
<template>
  <div class="form-container">
    <h2>Hydrogen Demand Calculator</h2>
    <form @submit.prevent="submitForm">
      <fieldset class="form-group" id="fleetPercentageFieldset">
        <legend>Percentage of Fleet Using Hydrogen:
          <span class="info-wrapper">
            <i class="info-icon">i</i>
            <span class="popup">
              Adjust this slider to set the percentage of your fleet that will be converted to hydrogen power
            </span>
          </span>
        </legend>
        <label for="fleetPercentage">{{ fleetPercentage }}%</label>
        <input id="fleetPercentage" type="range" v-model.number="fleetPercentage" min="0" max="100" step="1"
          class="slider" />
      </fieldset>

      <fieldset class="form-group" id="groundVehiclesFieldset">
        <legend>Ground Vehicles:
          <span class="info-wrapper">
            <i class="info-icon">i</i>
            <span class="popup">
              Select the types of ground support equipment vehicles to include in the hydrogen demand calculation
            </span>
          </span>
        </legend>
        <div id="groundVehicles" class="vehicle-list">
          <div v-for="(vehicle, index) in selectedVehicles" :key="index" class="vehicle-row"
            :id="'vehicle-row-' + index">
            <select v-model="vehicle.type" class="vehicle-type" :id="'vehicle-type-' + index">
              <option v-for="option in vehicleOptions" :key="option" :value="option"
                :disabled="isOptionDisabled(option, vehicle.type)">
                {{ option }}
              </option>
            </select>
            <button type="button" class="remove-btn" @click="removeVehicle(index)">
              ❌
            </button>
          </div>
        </div>
        <button type="button" class="add-btn" @click="addVehicle" :disabled="!canAddMoreVehicles"
          :class="{ 'disabled': !canAddMoreVehicles }" id="addVehicleButton">
          + Add Vehicle
        </button>
        <p v-if="!canAddMoreVehicles" class="no-vehicles-message" id="noVehiclesMessage">
          All available vehicles have been added
        </p>
      </fieldset>

      <fieldset class="form-group" id="endYearFieldset">
        <legend>Select End Year:
          <span class="info-wrapper">
            <i class="info-icon">i</i>
            <span class="popup">
              Choose the target year for implementing hydrogen infrastructure
            </span>
          </span>
        </legend>
        <div class="time-selection">
          <select v-model="selectedYear" id="selectedYear">
            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
          </select>
        </div>
      </fieldset>

      <button type="submit" id="calculateButton">Calculate</button>
    </form>

    <div v-if="isLoading" class="loading" id="loadingMessage">
      Loading...
    </div>
    <div v-if="results" class="results" id="resultsSection">
      <h3>Results:</h3>
      <p>
        Estimated Hydrogen Demand for Aircraft:
        {{ results?.aircraft_demand?.toFixed(2) || 0 }} ft³
      </p>
      <p>
        Estimated Hydrogen Demand for GSE:
        {{ results?.gse_demand?.total_h2_demand_vol_gse?.toFixed(2) || 0 }} ft³
      </p>
      <p>
        Total Estimated Hydrogen Demand:
        {{ results?.total_demand?.toFixed(2) || 0 }} ft³
      </p>

      <h3>Visualizations:</h3>
      <!-- Bar Chart: Aircraft vs. GSE Demand -->
      <div v-show="results.aircraft_demand && results.gse_demand?.total_h2_demand_vol_gse" class="chart-section"
        id="aircraftGseDemandChart">
        <h4>Aircraft vs. GSE Demand</h4>
        <Chart type="bar" :data="demandComparisonData" :options="demandComparisonOptions" />
      </div>

      <!-- Bar Chart: GSE Demand per Vehicle Type -->
      <div v-show="results.gse_demand?.gse_details?.length" class="chart-section" id="gseDemandPerVehicleChart">
        <h4>GSE Demand per Vehicle Type</h4>
        <Chart type="bar" :data="gseDemandPerVehicleData" :options="gseDemandPerVehicleOptions" />
      </div>

      <h3>Ground Support Equipment Details:</h3>
      <div v-for="(detail, index) in results?.gse_demand?.gse_details" :key="index" class="gse-detail"
        :id="'gse-detail-' + index">
        <p>Type: {{ detail.type }}</p>
        <p>Fuel Replaced: {{ detail.fuel_used }}</p>
        <p>Operating Time (Departure): {{ detail.operating_time_departure }} minutes</p>
        <p>Operating Time (Arrival): {{ detail.operating_time_arrival }} minutes</p>
        <p>
          Hydrogen Volume per Vehicle:
          {{ detail.hydrogen_volume_per_vehicle.toFixed(2) }} ft³
        </p>
      </div>
      <h3>Tank Specifications</h3>
      <div class="tank-specs">
        <dl>
          <dt>Tank Dimensions</dt>
          <dd>{{ tankSpecs.width }}ft (width) × {{ tankSpecs.length }}ft (length)</dd>

          <dt>Water Capacity</dt>
          <dd>{{ tankSpecs.waterCapacityGal }} gallons ({{ tankSpecs.waterCapacityFt3.toFixed(2) }} ft³)</dd>

          <dt>Ullage Factor</dt>
          <dd>{{ (tankSpecs.ullage * 100).toFixed(2) }}%</dd>

          <dt>Daily Evaporation Loss</dt>
          <dd>{{ (tankSpecs.evaporation * 100).toFixed(2) }}%</dd>

          <dt>Effective H₂ Storage per Tank</dt>
          <dd>{{ effectiveStorage.toFixed(2) }} ft³</dd>
        </dl>
      </div>
      <p>
        Number of Tanks Required:
        {{ tanksRequiredDisplay }}
      </p>
      <p>
        Storage Area Required:
        {{ results?.storage_area?.toFixed(2) || 0 }} ft²
      </p>
      <HydrogenMap :hydrogenStorageArea="results?.storage_area" :availableAreas="availableAreas" />
    </div>
    <div v-if="error" class="error" id="errorMessage">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { hydrogenService } from '../services/api.js';
import Chart from "@/components/Chart.vue";
import HydrogenMap from "@/components/HydrogenMap.vue";

// Reactive state
const fleetPercentage = ref(0);
const selectedVehicles = ref([]);
const selectedYear = ref("2025");
const results = ref(null);
const error = ref(null);
const vehicleOptions = ref([]);
const isLoading = ref(false); // Add isLoading state

const availableAreas = [
  // Airport Areas
  {
    name: "Terminal South Storage Area",
    type: "polygon",
    coordinates: [
      [33.6405, -84.4265],
      [33.6415, -84.4265],
      [33.6415, -84.4255],
      [33.6405, -84.4255],
    ],
    capacity: 20000 // Capacity in ft²
  },
  {
    name: "Terminal North Storage Area",
    type: "polygon",
    coordinates: [
      [33.6415, -84.4285],
      [33.6425, -84.4285],
      [33.6425, -84.4275],
      [33.6415, -84.4275],
    ],
    capacity: 15000 // Capacity in ft²
  },
  {
    name: "Cargo Area A",
    type: "polygon",
    coordinates: [
      [33.639, -84.429],
      [33.640, -84.429],
      [33.640, -84.428],
      [33.639, -84.428],
    ],
    capacity: 30000 // Capacity in ft²
  },
  {
    name: "Cargo Area B",
    type: "polygon",
    coordinates: [
      [33.638, -84.430],
      [33.639, -84.430],
      [33.639, -84.429],
      [33.638, -84.429],
    ],
    capacity: 25000 // Capacity in ft²
  },
  {
    name: "Service Area",
    type: "circle",
    center: [33.6402, -84.4272],
    radius: 100, // Radius in feet
    capacity: 18000 // Capacity in ft²
  },

  // Non-Airport Areas
  {
    name: "Downtown Hydrogen Facility",
    type: "circle",
    center: [33.749, -84.388],
    radius: 200, // Radius in feet
    capacity: 25000 // Capacity in ft²
  },
  {
    name: "East Side Storage Lot",
    type: "polygon",
    coordinates: [
      [33.748, -84.396],
      [33.749, -84.395],
      [33.751, -84.395],
      [33.752, -84.396],
      [33.751, -84.397],
      [33.749, -84.397]
    ],
    capacity: 8000 // Capacity in ft²
  },
  {
    name: "West Side Hydrogen Depot",
    type: "polygon",
    coordinates: [
      [33.652, -84.436],
      [33.653, -84.435],
      [33.653, -84.433],
      [33.652, -84.432],
      [33.651, -84.432],
      [33.651, -84.436]
    ],
    capacity: 12000 // Capacity in ft²
  },
  {
    name: "Northside Hydrogen Storage",
    type: "circle",
    center: [33.765, -84.388],
    radius: 300, // Radius in feet
    capacity: 10000 // Capacity in ft²
  },
  {
    name: "Southside Warehouse",
    type: "polygon",
    coordinates: [
      [33.613, -84.475],
      [33.614, -84.474],
      [33.615, -84.475],
      [33.615, -84.476],
      [33.613, -84.476]
    ],
    capacity: 6000 // Capacity in ft²
  }
];

// Fetch vehicle options from CSV
onMounted(async () => {
  await fetchVehicleOptions();
});

const fetchVehicleOptions = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/data/ground_fleet_data.csv");
    const csvData = response.data;
    const lines = csvData.split("\n");
    lines.shift(); // Remove header
    vehicleOptions.value = lines.map(line => line.split(",")[0]);
  } catch (err) {
    console.error("Error fetching vehicle options:", err);
  }
};

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
    const response = await hydrogenService.calculateTotalDemand({
      slider_perc: fleetPercentage.value / 100,
      gse: selectedVehicles.value,
      end_year: parseInt(selectedYear.value)
    });
    results.value = response;
    // Add storage area calculation
    if (results.value.total_demand) {
      results.value.storage_area = calculateStorageArea(
        results.value.total_demand
      );
    }
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

  if (!results.value ||
    !results.value.gse_demand ||
    !results.value.gse_demand.gse_details ||
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

// Add these reactive constants
const tankSpecs = ref({
  width: 10.1667,
  length: 56.5,
  waterCapacityGal: 18014,
  waterCapacityFt3: 18014 / 7.48052,
  ullage: 0.05,
  evaporation: 0.9925,
  material: "Stainless Steel",
  insulation: "Vacuum Super Insulation",
  maxPressure: "250 psi"
});

const effectiveStorage = computed(() => {
  return tankSpecs.value.waterCapacityFt3 *
    (1 - tankSpecs.value.ullage) *
    tankSpecs.value.evaporation;
});

const calculateStorageArea = (H2DemandVol) => {
  if (!H2DemandVol || H2DemandVol <= 0) return 0;

  const nbrTanks = Math.ceil(H2DemandVol / effectiveStorage.value); // Use ceil here for area calc
  return tankSpecs.value.width * tankSpecs.value.length * nbrTanks;
};

const numberOfTanks = computed(() => {
  if (!results.value?.total_demand || !effectiveStorage.value) return 0;
  return results.value.total_demand / effectiveStorage.value;
});

const tanksRequiredDisplay = computed(() => {
  if (!results.value?.total_demand || !effectiveStorage.value || effectiveStorage.value <= 0) {
    return "No tanks required";
  }

  const exactTanks = results.value.total_demand / effectiveStorage.value;
  const requiredTanks = Math.ceil(exactTanks);

  if (requiredTanks === 0) {
    return "0 tanks required";
  } else if (requiredTanks === 1) {
    return "1 tank required";
  } else {
    const lastTankUsage = ((exactTanks - (requiredTanks - 1)) * 100).toFixed(2);
    return `${requiredTanks} tanks required (${lastTankUsage}% usage for the last tank)`;
  }
});
</script>

<style scoped>
/* Container and overall layout */
.form-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 10px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Center the page title */
h2 {
  width: 100%;
  text-align: center;

}

/* Form group: using a set width and margin auto to center */
.form-group {
  width: 92%;
  max-width: 650px;
  margin: 0 auto 15px auto;
}

/* Range input styling */
input[type="range"] {
  width: 93%;
}

/* Legends */
.form-group legend {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

/* Vehicle row */
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

/* Remove button */
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

/* Add vehicle button */
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

/* Calculate button */
#calculateButton {
  display: block;
  margin: 0 15px 15px auto;
  width: 100%;
  max-width: 500px;
  padding: 14px;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

#calculateButton:hover {
  background: linear-gradient(135deg, #0056b3, #003d82);
  transform: scale(1.05);
}

/* Results block */
.results {
  margin-top: 20px;
  width: 95%;
  padding: 10px;
  background: #e9f5ff;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  color: #0056b3;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* GSE details */
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

/* Error block */
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

/* Chart section */
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

/* Info icon and popup styles  */
.info-wrapper {
  display: inline-block;
  position: relative;
  margin-left: 0px;
}

.info-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 12px;
  height: 15px;
  background: #007bff;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  cursor: help;
  font-style: normal;
  margin-left: 0;
}

.popup {
  visibility: hidden;
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  width: max-content;
  max-width: 200px;
  font-size: 12px;
  z-index: 100;
  opacity: 0;
  transition: opacity 0.3s, visibility 0.3s;
}

.info-wrapper:hover .popup {
  visibility: visible;
  opacity: 1;
}

.popup::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #333 transparent transparent transparent;
}

.results p {
  margin: 8px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.tank-specs {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin: 15px 0;
}

.tank-specs dl {
  display: grid;
  grid-template-columns: max-content auto;
  gap: 10px 15px;
}

.tank-specs dt {
  font-weight: 600;
  color: #2c3e50;
}

.tank-specs dd {
  margin: 0;
  color: #4a5568
}
</style>