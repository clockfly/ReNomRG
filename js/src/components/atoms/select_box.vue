<template>
  <select class="select-box"
    v-model="value"
    @input="$emit('input', $event.target.value)">
    <option v-for="(o, index) in options" :value="index" :key="index">
      {{ o }}
    </option>
  </select>
</template>

<script>
import { INPUT_WIDTH, INPUT_HEIGHT } from '@/const'

export default {
  name: 'SelectBox',
  props: {
    value: {},
    options: {
      type: Array
    },
    w: {
      type: String,
      default: INPUT_WIDTH
    },
    h: {
      type: String,
      default: INPUT_HEIGHT
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
