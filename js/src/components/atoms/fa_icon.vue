<template>
  <i :class="cls" aria-hidden="true"
    v-bind:style="{ 'color': textcolor }"></i>
</template>

<script>
import { BLACK } from '@/const'

export default {
  name: 'FaIcon',
  props: {
    cls: { type: String, required: true },
    textcolor: { type: String, default: BLACK }
  }
}
</script>

<style lang="scss" scoped>
</style>
