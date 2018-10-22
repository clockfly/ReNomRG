<template>
  <button
    v-bind:style="{
      width: w,
      height: h,
      background: backgroundcolor,
      color: textcolor }"
    @click="click">
    <slot name="icon"></slot>
    {{text}}
  </button>
</template>

<script>
import { BLUE, WHITE } from '@/const'

export default {
  name: 'Button',
  props: {
    text: {
      type: String,
      required: true
    },
    w: {
      type: String,
      default: '88px'
    },
    h: {
      type: String,
      default: '44px'
    },
    backgroundcolor: {
      type: String,
      default: BLUE
    },
    textcolor: {
      type: String,
      default: WHITE
    }
  },
  methods: {
    click: function () {
      this.$emit('click')
    }
  }
}
</script>

<style lang="scss" scoped>
button {
  border: none;
}
</style>
