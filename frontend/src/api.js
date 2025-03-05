// frontend/src/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

export async function submitHydrogenDemand(data) {
  try {
    const response = await axios.post(`${API_BASE_URL}/h2_demand`, data);
    return response.data;
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
