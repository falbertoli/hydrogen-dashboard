<!-- frontend/src/components/HydrogenMap.vue -->
<template>
  <div id="map" style="height: 400px;"></div>
</template>

<script>
import { onMounted, ref, watch, onBeforeUnmount } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
  props: {
    compliantZones: {
      type: Array,
      required: true,
    },
    requiredStorageArea: {
      type: Number,
      required: false
    }
  },
  setup(props) {
    const map = ref(null);

    onMounted(() => {
      // Atlanta Airport Coordinates
      const atlantaAirportLat = 33.6407;   // Latitude of Atlanta Airport
      const atlantaAirportLng = -84.4277;  // Longitude of Atlanta Airport
      const zoomLevel = 13;             // Adjust zoom level as needed

      map.value = L.map('map').setView([atlantaAirportLat, atlantaAirportLng], zoomLevel);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map.value);

      watch(() => props.compliantZones, (newCompliantZones) => {
        if (map.value) {
          map.value.eachLayer((layer) => {
            if (layer instanceof L.Polygon) {
              map.value.removeLayer(layer);
            }
          });
        }

        newCompliantZones.forEach(zone => {
          if (zone.coordinates && Array.isArray(zone.coordinates)) {
            const polygon = L.polygon(zone.coordinates, {
              color: 'blue',
              fillColor: 'lightblue',
              fillOpacity: 0.5
            }).addTo(map.value).bindPopup(zone.name);
          } else {
            console.warn("Invalid coordinates data:", zone);
          }
        });
      }, { immediate: true });

      onBeforeUnmount(() => {
        if (map.value) {
          map.value.remove();
          map.value = null;
        }
      });
    });

    return { map };
  },
};
</script>