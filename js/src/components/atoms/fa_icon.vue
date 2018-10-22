<template>
  <i :class="cls" aria-hidden="true"
    v-bind:style="{ 'color': textcolor }"></i>
</template>

<script>
import { TEXT_COLOR } from '@/const'

export default {
  name: 'FaIcon',
  props: {
    cls: {
      type: String,
      required: true
    },
    textcolor: {
      type: String,
      default: TEXT_COLOR
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
