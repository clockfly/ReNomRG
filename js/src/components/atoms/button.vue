<template>
  <button
    v-bind:style="{
      width: w,
      height: h,
      background: backgroundcolor,
      color: textcolor }"
    @click="$emit('click')">
    <slot name="icon"></slot>
    {{text}}
  </button>
</template>

<script>
import { BLUE, WHITE, BUTTON_WIDTH, BUTTON_HEIGHT } from '@/const'

export default {
  name: 'Button',
  props: {
    text: {
      type: String,
      required: true
    },
    w: {
      type: String,
      default: BUTTON_WIDTH
    },
    h: {
      type: String,
      default: BUTTON_HEIGHT
    },
    backgroundcolor: {
      type: String,
      default: BLUE
    },
    textcolor: {
      type: String,
      default: WHITE
    }
  }
}
</script>

<style lang="scss" scoped>
button {
  border: none;
}
</style>
