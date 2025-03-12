// src/services/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api";

export const hydrogenService = {
  async calculateTotalDemand(data) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/hydrogen-demand/total`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error calculating total hydrogen demand:", error);
      throw error;
    }
  },

  async calculateAircraftDemand(data) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/hydrogen-demand/aircraft`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error calculating aircraft hydrogen demand:", error);
      throw error;
    }
  },

  async calculateGseDemand(data) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/hydrogen-demand/gse`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error calculating GSE hydrogen demand:", error);
      throw error;
    }
  },
};

export const storageService = {
  async calculateStorageCost(data) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/storage/calculate`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error calculating storage cost:", error);
      throw error;
    }
  },
};

export const economicService = {
  async calculateEconomicImpact(data) {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/economic/impact`,
        data
      );
      return response.data;
    } catch (error) {
      console.error("Error calculating economic impact:", error);
      throw error;
    }
  },
};

export default {
  hydrogenService,
  storageService,
  economicService,
};
