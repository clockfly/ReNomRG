<template>
  <div class="clickable_text"
    v-bind:style="{ 'color': textcolor }"
    @click="$emit('click')">
    <slot name="icon"></slot>
    <PlainText
      :text="text"
      :textcolor="textcolor">
    </PlainText>
  </div>
</template>

<script>
import { BLACK } from '@/const'
import PlainText from '@/components/atoms/plain_text'

export default {
  name: 'ClickableText',
  components: {
    PlainText
  },
  props: {
    text: {},
    textcolor: { type: String, default: BLACK }
  }
}
</script>

<style lang="scss" scoped>
.clickable_text {
  @include prefix("display", "flex");
}
</style>
