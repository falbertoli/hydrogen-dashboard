<!-- total_h2_volume_gal,        # Total hydrogen volume to store [gallons]
    number_of_tanks,            # Number of tanks
    tank_diameter_ft,           # Diameter of each cylindrical tank [ft]
    tank_length_ft,             # Length of each cylindrical tank [ft]
    cost_per_sqft_construction, # Construction cost [$/ft^2]
    cost_per_cuft_insulation  -->
<template>
  <div class="formcontainer">
    <h1>Storage Cost Calculator</h1>
    <form @submit.prevent="submitForm">
      <fieldset id="totalH2volumeField">
        <legend id="totalH2Volume">
          <label for="total_h2_volume_gal">Total Hydrogen Volume to Store [gallons]</label>
          <input type="number" id="total_h2_volume_gal" name="total_h2_volume_gal" v-model="total_h2_volume_gal">
        </legend>
      </fieldset>
    </form>

  </div>
</template>

<script>
export default {

}
</script>

<style></style>