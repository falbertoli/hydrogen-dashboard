<!-- frontend/src/components/Chart.vue -->
<template>
  <div class="chart-container" v-if="isDataValid">
    <component :is="chartComponent" :data="chartData" :options="mergedOptions" />
  </div>
  <div v-else class="no-chart-data">
    No chart data available
  </div>
</template>

<script setup>
import { defineProps, computed, ref } from "vue";
import { Bar, Line, Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  ArcElement,
} from "chart.js";

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LineElement, PointElement, ArcElement);

const props = defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ["bar", "line", "pie"].includes(value),
  },
  data: {
    type: Object,
    default: () => ({
      labels: [],
      datasets: []
    })
  },
  options: {
    type: Object,
    default: () => ({})
  }
});

const chartComponent = computed(() => {
  switch (props.type) {
    case "bar":
      return Bar;
    case "line":
      return Line;
    case "pie":
      return Pie;
    default:
      return Bar;
  }
});

const isDataValid = computed(() => {
  return props.data &&
    props.data.labels &&
    Array.isArray(props.data.labels) &&
    props.data.datasets &&
    Array.isArray(props.data.datasets);
});

const chartData = computed(() => {
  if (!isDataValid.value) {
    return {
      labels: [],
      datasets: []
    };
  }
  return props.data;
});

const mergedOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    ...(props.options || {})
  };
});
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}

.no-chart-data {
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #777;
  border: 1px dashed #ccc;
  border-radius: 8px;
}
</style>