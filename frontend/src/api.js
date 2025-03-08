// frontend/src/api.js
/*
 * How to use in Vue (import api from "./api.js";)
 * Imporrt the functions: Import these functions in the script section of the Vue component where you want to use them = Where you want to make the API call.
 * Call the functions: Call the functions in the methods section of the Vue component. Use the functions to make the API calls.
 */
import axios from "axios"; // Import axios library. Simplifies HTTP requests in JavaScript.

const API_BASE_URL = "http://127.0.0.1:5000";

export async function submitHydrogenDemand(data) {
  /* Function to submit hydrogen demand data to the backend.
  Args:
    data: JSON object containing hydrogen demand data. Parameters needed for the /h2_demand endpoint.
  Returns:
    JSON object containing hydrogen demand results.
  NOTE: try...catch block is used to handle errors. If an error occurs, it is logged to the console and re-thrown.
  */
  try {
    const response = await axios.post(`${API_BASE_URL}/h2_demand`, data); // Send POST request to /h2_demand endpoint. 'await' waits for the response to be received.
    return response.data; // Extracts the JSON data from the server's response. Returns the JSON object = extracted data.
  } catch (error) {
    console.error("Error fetching hydrogen demand results:", error);
    throw error;
  }
}

export async function submitHydrogenDemandGSE(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/h2_demand_gse`, data);
    return response.data;
  } catch (error) {
    console.error(
      "Error fetching ground support equipment hydrogen demand results:",
      error
    );
    throw error;
  }
}

export async function submitHydrogenDemandAC(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/h2_demand_ac`, data);
    return response.data;
  } catch (error) {
    console.error("Error fetching aircraft hydrogen demand results:", error);
    throw error;
  }
}

export async function submitStorage(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/storage_cost`, data);
    return response.data;
  } catch (error) {
    console.error("Error fetching storage results:", error);
    throw error;
  }
}

export async function submitFinancialAnalysis(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/economic_impact`, data);
    return response.data;
  } catch (error) {
    console.error("Error fetching financial analysis results:", error);
    throw error;
  }
}

export default {
  submitHydrogenDemand,
  submitHydrogenDemandGSE,
  submitHydrogenDemandAC,
  submitStorage,
  submitFinancialAnalysis,
};

/*
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
*/
