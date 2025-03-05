// frontend/src/composables/useHydrogenCalculator.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // Ensure this matches your backend URL

export async function submitHydrogenDemand(
  fleetPercentage,
  selectedVehicles,
  selectedTimePeriod
) {
  try {
    const response = await axios.post(`${API_BASE_URL}/h2_demand_gse`, {
      database_name: "aircraft_data.db",
      gse: selectedVehicles,
      end_year: selectedTimePeriod,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching hydrogen demand results:", error);
    throw error; // Re-throw the error to be caught in the component
  }
}

export async function submitStorage(storageArea) {
  try {
    const response = await axios.post(`${API_BASE_URL}/storage_cost`, {
      total_h2_volume_gal: storageArea.total_h2_volume_gal,
      number_of_tanks: storageArea.number_of_tanks,
      tank_diameter_ft: storageArea.tank_diameter_ft,
      tank_length_ft: storageArea.tank_length_ft,
      cost_per_sqft_construction: storageArea.cost_per_sqft_construction,
      cost_per_cuft_insulation: storageArea.cost_per_cuft_insulation,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching storage results:", error);
    throw error; // Re-throw the error to be caught in the component
  }
}

export async function submitFinancialAnalysis(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/economic_impact`, {
      d: data.d,
      tax_credits: data.tax_credits,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching financial analysis results:", error);
    throw error; // Re-throw the error to be caught in the component
  }
}
