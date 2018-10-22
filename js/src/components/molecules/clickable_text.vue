<template>
  <div class="clickable_text"
    v-bind:style="{ 'color': textcolor }"
    @click="click">
    <slot name="icon"></slot>
    <PlainText
      :text="text"
      :textcolor="textcolor">
    </PlainText>
  </div>
</template>

<script>
import { TEXT_COLOR } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'ClickableText',
  components: {
    PlainText
  },
  props: {
    text: {
      type: String
    },
    textcolor: {
      type: String,
      default: TEXT_COLOR
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
</style>
