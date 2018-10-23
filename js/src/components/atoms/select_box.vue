<template>
  <select class="select-box"
    v-model="selected"
    @change="$emit('change', selected)">
    <option v-for="(o, index) in options" :value="index" :key="index">
      {{ o }}
    </option>
  </select>
</template>

<script>
import { INPUT_WIDTH, INPUT_HEIGHT } from '@/const'

export default {
  name: 'SelectBox',
  data: function () {
    return {
      'selected': 0
    }
  },
  props: {
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
