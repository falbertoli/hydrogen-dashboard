<!-- frontend/src/views/CostAnalysisView.vue -->
<template>
  <div id="cost-analysis-view">
    <h1>Cost Analysis</h1>
    <CostAnalysisForm />

  </div>
</template>

<script>
import CostAnalysisForm from '@/components/CostAnalysisForm.vue';

export default {
  components: {
    CostAnalysisForm,
  },
};
</script>

<style scoped>
#cost-analysis-view {
  padding: 20px;
}
</style>
