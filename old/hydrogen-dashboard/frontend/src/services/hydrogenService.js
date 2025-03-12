// Hydrogen Demand API calls
import api from "./api";
import { ENDPOINTS } from "../constants/apiEndpoints";

export const hydrogenService = {
  /**
   * Calculate aircraft hydrogen demand
   * @param {Object} params - Parameters for calculation
   * @returns {Promise} - API response
   */
  calculateAircraftDemand(params) {
    return api.post(ENDPOINTS.HYDROGEN_DEMAND.AIRCRAFT, params);
  },

  /**
   * Calculate GSE hydrogen demand
   * @param {Object} params - Parameters for calculation
   * @returns {Promise} - API response
   */
  calculateGseDemand(params) {
    return api.post(ENDPOINTS.HYDROGEN_DEMAND.GSE, params);
  },

  /**
   * Calculate total hydrogen demand (aircraft + GSE)
   * @param {Object} params - Parameters for calculation
   * @returns {Promise} - API response
   */
  calculateTotalDemand(params) {
    return api.post(ENDPOINTS.HYDROGEN_DEMAND.TOTAL, params);
  },
};
