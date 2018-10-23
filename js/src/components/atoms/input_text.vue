<template>
  <input type="text"
    :placeholder="placeholder"
    v-model="localtext"
    @change="$emit('change', localtext)">
</template>

<script>
import { INPUT_WIDTH, INPUT_HEIGHT } from '@/const'

export default {
  name: 'InputText',
  data: function () {
    return {
      'localtext': ''
    }
  },
  props: {
    placeholder: {
      type: String
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
