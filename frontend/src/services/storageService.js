// Storage API calls
import api from "./api";
import { ENDPOINTS } from "../constants/apiEndpoints";

export const storageService = {
  /**
   * Calculate storage costs
   * @param {Object} params - Parameters for calculation
   * @returns {Promise} - API response
   */
  calculateStorageCost(params) {
    return api.post(ENDPOINTS.STORAGE.CALCULATE, params);
  },
};
