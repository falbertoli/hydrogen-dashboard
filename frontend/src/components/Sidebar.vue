<template>
  <div class="sidebar">
    <h2>Dashboard</h2>
    <ul>
      <li><router-link to="/">Overview</router-link></li>
      <li><router-link to="/hydrogen-demand">Hydrogen Demand</router-link></li>
      <li><router-link to="/storage">Storage</router-link></li>
      <li><router-link to="/cost-analysis">Cost Analysis</router-link></li>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 20px;
  height: 100vh;
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
</style>
