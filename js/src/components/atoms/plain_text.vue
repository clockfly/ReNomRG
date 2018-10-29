<template>
  <div class="plain-text"
    v-bind:style="{
      'width': w,
      'height': h,
      'color': textcolor,
      'font-size': fontsize,
      'font-weight': fontweight,
      'line-height': h }">
    {{text}}
  </div>
</template>

<script>
import { BLACK, TEXT_FONT_SIZE } from '@/const'

export default {
  name: 'PlainText',
  props: {
    text: {},
    w: { type: String },
    h: { type: String },
    textcolor: { type: String, default: BLACK },
    fontsize: { type: String, default: TEXT_FONT_SIZE },
    fontweight: { type: String, default: 'normal' }
  }
}
</script>

<style lang="scss" scoped>
</style>
