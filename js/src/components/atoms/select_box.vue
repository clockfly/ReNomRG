<template>
  <select class="select-box"
    v-bind:style="{
      'width': w,
      'height': h,
      'padding': padding,
      'background': backgroundcolor,
      'color': textcolor,
      'font-size': fontsize }"
    v-model="value"
    @input="$emit('input', $event.target.value)">
    <option v-for="(o, index) in options" :value="index" :key="index">
      {{ o }}
    </option>
  </select>
</template>

<script>
import { BLACK, WHITE, INPUT_WIDTH, INPUT_HEIGHT, INPUT_FONT_SIZE } from '@/const'

export default {
  name: 'SelectBox',
  props: {
    value: {},
    options: { type: Array },
    w: { type: String, default: INPUT_WIDTH },
    h: { type: String, default: INPUT_HEIGHT },
    padding: { type: String, default: '0' },
    backgroundcolor: { type: String, default: WHITE },
    textcolor: { type: String, default: BLACK },
    fontsize: { type: String, default: INPUT_FONT_SIZE }
  }
}
</script>

<style lang="scss" scoped>
</style>
