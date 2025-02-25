<template>
  <div>
    <h2>Atlanta Airport - Hydrogen Storage Areas</h2>
    <l-map :zoom="zoom" :center="center" style="height: 600px; width: 100%">
      <l-tile-layer :url="tileLayer" />
      <!-- Show compliant zones based on backend calculation -->
      <l-polygon
        v-for="(zone, index) in compliantZones"
        :key="index"
        :lat-lngs="zone.coordinates"
        color="green"
        fill-opacity="0.3"
      >
        <l-popup>{{ zone.name }} - Free Space: {{ zone.space }} ft²</l-popup>
      </l-polygon>
    </l-map>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer, LPolygon } from '@vue-leaflet/vue-leaflet';

export default {
  props: ['requiredStorageArea'],
  components: {
    LMap,
    LTileLayer
  },
  data() {
    return {
      zoom: 15,
      center: [33.6407, -84.4277], // Atlanta Airport coordinates
      tileLayer: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      compliantZones: [] // Will be populated with backend results
    };
  },
  methods: {
    async fetchCompliantZones() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/calculate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            fleetPercentage: 50, // Example values
            selectedVehicles: [{ type: 'Pickup Truck', count: 5 }],
            selectedTimePeriod: "7 days"
          }),
        });
        const data = await response.json();
        this.compliantZones = data.compliantZones;
      } catch (error) {
        console.error("Error fetching zones:", error);
      }
    }
  },
  mounted() {
    this.fetchCompliantZones();
  }
};
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #0056b3;
}
</style>
