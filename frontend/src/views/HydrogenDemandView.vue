<!-- frontend/src/views/HydrogenDemandView.vue -->
<template>
  <div class="form-container">
    <h1>Hydrogen Demand</h1>
    <HydrogenDemandForm />
  </div>
</template>

<script>
import HydrogenDemandForm from "../components/HydrogenDemandForm.vue";

export default {
  components: {
    HydrogenDemandForm,
  },
};
</script>
