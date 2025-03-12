// Economic impact state and logic
import { ref, computed, reactive } from "vue";
import { economicService } from "../services/economicService";

export function useEconomicState() {
  // State
  const loading = ref(false);
  const error = ref(null);
  const results = ref(null);

  // Form data
  const form = reactive({
    fleet_percentage: 0.3,
    total_flights: 100000,
    atlanta_fraction: 0.4,
    hydrogen_demand: 5000000,
    turnaround_time: 30,
    tax_credits: 0.1,
  });

  // Computed properties
  const revenueDrop = computed(() => {
    if (!results.value) return 0;
    return results.value.revenue_drop;
  });

  // Methods
  const calculateEconomicImpact = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await economicService.calculateEconomicImpact(form);
      results.value = response.data;
    } catch (err) {
      error.value = err.message || "An error occurred";
      console.error("Error calculating economic impact:", err);
    } finally {
      loading.value = false;
    }
  };

  const resetForm = () => {
    form.fleet_percentage = 0.3;
    form.total_flights = 100000;
    form.atlanta_fraction = 0.4;
    form.hydrogen_demand = 5000000;
    form.turnaround_time = 30;
    form.tax_credits = 0.1;
    results.value = null;
    error.value = null;
  };

  return {
    // State
    loading,
    error,
    results,
    form,

    // Computed
    revenueDrop,

    // Methods
    calculateEconomicImpact,
    resetForm,
  };
}
