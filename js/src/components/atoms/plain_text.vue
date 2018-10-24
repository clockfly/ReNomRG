<template>
  <div class="plain_text"
    v-bind:style="{ 'color': textcolor }">
    {{text}}
  </div>
</template>

<script>
import { BLACK } from '@/const'

export default {
  name: 'PlainText',
  props: {
    text: {},
    textcolor: { type: String, default: BLACK }
  }
}
</script>

<style lang="scss" scoped>
</style>
