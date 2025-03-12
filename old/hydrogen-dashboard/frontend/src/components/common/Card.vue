<template>
  <div class="card">
    <div v-if="title" class="card-header">
      {{ title }}
    </div>
    <div class="card-body">
      <h5 v-if="subtitle" class="card-title">{{ subtitle }}</h5>
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  props: {
    title: {
      type: String,
      default: ''
    },
    subtitle: {
      type: String,
      default: ''
    }
  }
}
</script>