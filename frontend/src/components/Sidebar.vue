<!-- frontend/src/components/Sidebar.vue -->
<template>
  <div>
    <button @click="toggleSidebar" class="toggle-button">
      <span class="hamburger-icon"></span>
      <span class="hamburger-icon"></span>
      <span class="hamburger-icon"></span>
    </button>
    <div v-if="isSidebarVisible" class="sidebar">
      <h2>Dashboard</h2>
      <ul>
        <li><router-link to="/">Overview</router-link></li>
        <li><router-link to="/hydrogen-demand">Hydrogen Demand</router-link></li>
        <!-- <li><router-link to="/regulations">Regulations</router-link></li> -->
        <li><router-link to="/storage-space">Storage Space</router-link></li>
        <!-- <li><router-link to="/cost-analysis">Cost Analysis</router-link></li>
        <li><router-link to="/storage-cost">Storage Cost</router-link></li>
        <li><router-link to="/sustainability">Sustainability Analysis</router-link></li>     -->

      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isSidebarVisible = ref(true);

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value;
};
</script>

<style scoped>
.toggle-button {
  position: fixed;
  top: 10px;
  left: 10px;
  padding: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: auto;
  /* Ensure the button width is limited to its content */
}

.hamburger-icon {
  display: block;
  width: 25px;
  height: 3px;
  background-color: #007bff;
  margin: 4px 0;
  transition: all 0.3s ease-in-out;
}

.toggle-button:hover .hamburger-icon {
  background-color: #0056b3;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 20px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
}

h2 {
  color: white;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 15px 0;
}

a {
  color: white;
  text-decoration: none;
}

a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}

.sidebar a {
  display: block;
  color: white;
  text-decoration: none;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition: background 0.3s;
}

.sidebar a:hover {
  background: #34495e;
}
</style>
