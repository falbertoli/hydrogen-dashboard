// Economic impact API calls
import api from "./api";
import { ENDPOINTS } from "../constants/apiEndpoints";

export const economicService = {
  /**
   * Calculate economic impact
   * @param {Object} params - Parameters for calculation
   * @returns {Promise} - API response
   */
  calculateEconomicImpact(params) {
    return api.post(ENDPOINTS.ECONOMIC.IMPACT, params);
  },
};
