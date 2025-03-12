// Hydrogen Demand state and logic
import { ref, computed, reactive } from "vue";
import { hydrogenService } from "../services/hydrogenService";

export function useHydrogenDemandState() {
  // State
  const loading = ref(false);
  const error = ref(null);
  const results = ref(null);

  // Form data
  const form = reactive({
    slider_perc: 0.5,
    end_year: 2030,
    gse: [{ type: "Baggage Tractor" }, { type: "Belt Loader" }],
  });

  // Computed properties
  const totalDemand = computed(() => {
    if (!results.value) return 0;
    return results.value.total_demand;
  });

  // Methods
  const calculateDemand = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await hydrogenService.calculateTotalDemand(form);
      results.value = response.data;
    } catch (err) {
      error.value = err.message || "An error occurred";
      console.error("Error calculating hydrogen demand:", err);
    } finally {
      loading.value = false;
    }
  };

  const resetForm = () => {
    form.slider_perc = 0.5;
    form.end_year = 2030;
    form.gse = [{ type: "Baggage Tractor" }, { type: "Belt Loader" }];
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
    totalDemand,

    // Methods
    calculateDemand,
    resetForm,
  };
}
