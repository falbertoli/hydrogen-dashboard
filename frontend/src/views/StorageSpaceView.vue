<!-- frontend/src/views/HydrogenDemandView.vue -->
<template>
  <div class="form-container">
    <h1>Storage Space</h1>
    <HydrogenDemandForm />
  </div>
</template>

<script>
import StorageSpaceForm from '@/components/StorageSpaceForm.vue';

export default {
  name: 'StorageSpaceView',
  components: {
    StorageSpaceForm,
  },
};
</script>
