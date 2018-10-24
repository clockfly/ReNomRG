<template>
  <input type="text"
    :placeholder="placeholder"
    :value="value"
    @input="$emit('input', $event.target.value)">
</template>

<script>
import { INPUT_WIDTH, INPUT_HEIGHT } from '@/const'

export default {
  name: 'InputText',
  props: {
    value: {},
    placeholder: { type: String },
    w: { type: String, default: INPUT_WIDTH },
    h: { type: String, default: INPUT_HEIGHT }
  }
}
</script>

<style lang="scss" scoped>
</style>
