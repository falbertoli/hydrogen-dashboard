<template>
  <div class="alert alert-danger" role="alert">
    <strong v-if="title">{{ title }}</strong>
    <p v-if="message">{{ message }}</p>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    title: {
      type: String,
      default: 'Error'
    },
    message: {
      type: String,
      default: ''
    }
  }
}
</script>