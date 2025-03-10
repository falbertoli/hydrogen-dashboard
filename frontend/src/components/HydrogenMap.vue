<template>
  <div id="map" style="height: 400px;"></div>
</template>

<script>
import { onMounted, ref, watch, onBeforeUnmount } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
  props: {
    hydrogenStorageArea: {
      type: Number,
      required: true,
    },
    availableAreas: {
      type: Array,
      required: true,
    }
  },
  setup(props) {
    const map = ref(null);

    onMounted(() => {
      const atlantaAirportLat = 33.6407;   // Latitude of Atlanta Airport
      const atlantaAirportLng = -84.4277;  // Longitude of Atlanta Airport
      const zoomLevel = 13;                 // Adjust zoom level as needed

      map.value = L.map('map').setView([atlantaAirportLat, atlantaAirportLng], zoomLevel);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map.value);

      // Watch the available areas and hydrogen storage area
      watch(() => props.availableAreas, (newAreas) => {
        if (map.value) {
          clearLayers();

          newAreas.forEach(area => {
            let layer;
            let areaSize;

            if (area.type === 'polygon') {
              areaSize = calculatePolygonArea(area.coordinates);
              layer = L.polygon(area.coordinates, {
                color: getAreaColor(areaSize, area.capacity),
                fillColor: getAreaColor(areaSize, area.capacity),
                fillOpacity: 0.5,
                zIndex: 2 // Set zIndex higher for polygons
              }).addTo(map.value).bindPopup(`${area.name}<br>Area: ${areaSize.toFixed(2)} ft²<br>Capacity: ${area.capacity} ft²`);
            } else if (area.type === 'circle') {
              areaSize = calculateCircleArea(area.radius);
              layer = L.circle(area.center, {
                radius: area.radius,
                color: getAreaColor(areaSize, area.capacity),
                fillColor: getAreaColor(areaSize, area.capacity),
                fillOpacity: 0.5,
                zIndex: 1 // Set zIndex lower for circles
              }).addTo(map.value).bindPopup(`${area.name}<br>Area: ${areaSize.toFixed(2)} ft²<br>Capacity: ${area.capacity} ft²`);
            }
          });
        }
      }, { immediate: true });

      onBeforeUnmount(() => {
        if (map.value) {
          map.value.remove();
          map.value = null;
        }
      });
    });

    const clearLayers = () => {
      if (map.value) {
        map.value.eachLayer((layer) => {
          if (layer instanceof L.Polygon || layer instanceof L.Circle) {
            map.value.removeLayer(layer);
          }
        });
      }
    };

    const getAreaColor = (areaSize, capacity) => {
      if (capacity >= props.hydrogenStorageArea) {
        return '#28a745';  // Green: can accommodate the hydrogen storage area
      } else if (capacity >= props.hydrogenStorageArea * 0.8) {
        return '#ffc107';  // Yellow: close to accommodating but not quite enough
      } else {
        return '#dc3545';  // Red: cannot accommodate the hydrogen storage area
      }
    };

    const calculatePolygonArea = (coordinates) => {
      // Using the shoelace formula to calculate area of polygon
      let area = 0;
      const n = coordinates.length;

      for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        area += coordinates[i][0] * coordinates[j][1];
        area -= coordinates[j][0] * coordinates[i][1];
      }
      area = Math.abs(area) / 2;
      return area; // Area in square feet
    };

    const calculateCircleArea = (radius) => {
      return Math.PI * Math.pow(radius, 2); // Area in square feet
    };

    return { map };
  },
};
</script>

<style scoped>
#map {
  height: 100%;
}
</style>