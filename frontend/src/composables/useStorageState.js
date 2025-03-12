// Storage state and logic
import { ref, computed, reactive } from "vue";
import { storageService } from "../services/storageService";

export function useStorageState() {
  // State
  const loading = ref(false);
  const error = ref(null);
  const results = ref(null);

  // Form data
  const form = reactive({
    total_h2_volume_gal: 5000000,
    number_of_tanks: 20,
    tank_diameter_ft: 10,
    tank_length_ft: 40,
    cost_per_sqft_construction: 580,
    cost_per_cuft_insulation: 15,
  });

  // Computed properties
  const totalCost = computed(() => {
    if (!results.value) return 0;
    return results.value.total_infrastructure_cost;
  });

  // Methods
  const calculateStorageCost = async () => {
    loading.value = true;
    error.value = null;

    try {
      const response = await storageService.calculateStorageCost(form);
      results.value = response.data;
    } catch (err) {
      error.value = err.message || "An error occurred";
      console.error("Error calculating storage cost:", err);
    } finally {
      loading.value = false;
    }
  };

  const resetForm = () => {
    form.total_h2_volume_gal = 5000000;
    form.number_of_tanks = 20;
    form.tank_diameter_ft = 10;
    form.tank_length_ft = 40;
    form.cost_per_sqft_construction = 580;
    form.cost_per_cuft_insulation = 15;
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
    totalCost,

    // Methods
    calculateStorageCost,
    resetForm,
  };
}
