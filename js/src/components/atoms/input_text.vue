<template>
  <input type="text"
    v-bind:style="{
      'width': w,
      'height': h,
      'padding': padding,
      'border': borderwidth+' '+bordertype+' '+bordercolor,
      'background': backgroundcolor,
      'color': textcolor,
      'font-size': fontsize }"
    :placeholder="placeholder"
    :value="value"
    @input="$emit('input', $event.target.value)">
</template>

<script>
import { BLACK, GRAY, WHITE, INPUT_WIDTH, INPUT_HEIGHT, INPUT_FONT_SIZE } from '@/const'

export default {
  name: 'InputText',
  props: {
    value: {},
    placeholder: { type: String },
    w: { type: String, default: INPUT_WIDTH },
    h: { type: String, default: INPUT_HEIGHT },
    padding: { type: String, default: '0' },
    borderwidth: { type: String, default: '1px' },
    bordertype: { type: String, default: 'solid' },
    bordercolor: { type: String, default: GRAY },
    backgroundcolor: { type: String, default: WHITE },
    textcolor: { type: String, default: BLACK },
    fontsize: { type: String, default: INPUT_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
</style>
