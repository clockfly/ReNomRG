<template>
  <div class="plain_text"
    v-bind:style="{ 'color': textcolor }">
    {{text}}
  </div>
</template>

<script>
import { TEXT_COLOR } from '@/const'

export default {
  name: 'PlainText',
  props: {
    text: {
      type: String
    },
    textcolor: {
      type: String,
      default: TEXT_COLOR
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
