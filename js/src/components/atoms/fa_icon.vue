<template>
  <i :class="cls" aria-hidden="true"
    v-bind:style="{
      'height': h,
      'color': textcolor,
      'font-size': fontsize,
      'line-height': h }"></i>
</template>

<script>
import { BLACK, TEXT_FONT_SIZE } from '@/const'

export default {
  name: 'FaIcon',
  props: {
    cls: { type: String, required: true },
    h: { type: String },
    textcolor: { type: String, default: BLACK },
    fontsize: { type: String, default: TEXT_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
</style>
