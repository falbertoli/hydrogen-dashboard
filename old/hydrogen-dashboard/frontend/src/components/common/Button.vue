<template>
  <button :class="[
    'btn',
    `btn-${type}`,
    { 'btn-block': block, 'btn-lg': large, 'btn-sm': small }
  ]" :disabled="loading || disabled" @click="$emit('click', $event)">
    <span v-if="loading" class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'].includes(value)
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    block: {
      type: Boolean,
      default: false
    },
    large: {
      type: Boolean,
      default: false
    },
    small: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click']
}
</script>