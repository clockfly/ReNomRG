<template>
  <button
    v-bind:style="{
      'width': w,
      'height': h,
      'padding': padding,
      'border': borderwidth+' '+bordertype+' '+bordercolor,
      'background': backgroundcolor,
      'color': textcolor,
      'font-size': fontsize }"
    @click="$emit('click')">
    <div class="button-text">
      <slot name="icon"></slot>
      {{text}}
    </div>
  </button>
</template>

<script>
import { BLUE, WHITE, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_FONT_SIZE } from '@/const'

export default {
  name: 'Button',
  props: {
    text: { type: String, default: 'Submit' },
    w: { type: String, default: BUTTON_WIDTH },
    h: { type: String, default: BUTTON_HEIGHT },
    padding: { type: String, default: '0' },
    borderwidth: { type: String, default: '1px' },
    bordertype: { type: String, default: 'solid' },
    bordercolor: { type: String, default: BLUE },
    backgroundcolor: { type: String, default: BLUE },
    textcolor: { type: String, default: WHITE },
    fontsize: { type: String, default: BUTTON_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
</style>
