import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

export async function submitHydrogenDemand(fleetPercentage, selectedVehicles, selectedTimePeriod) {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/calculate`, {
      calculationMode: "demand",
      fleetPercentage,
      selectedVehicles,
      selectedTimePeriod
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching hydrogen demand results:", error);
    return null;
  }
}

export async function submitStorage(storageArea) {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/calculate`, {
      calculationMode: "storage",
      storageArea
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching storage results:", error);
    return null;
  }
}
